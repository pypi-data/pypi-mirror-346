"""Jarvis代码代理模块。

该模块提供CodeAgent类，用于处理代码修改任务。
"""

import os
import sys
import subprocess
import argparse
from typing import Any, Dict, Optional, List, Tuple

# 忽略yaspin的类型检查
from yaspin import yaspin  # type: ignore

from jarvis.jarvis_agent import Agent
from jarvis.jarvis_agent.builtin_input_handler import builtin_input_handler
from jarvis.jarvis_agent.file_input_handler import file_input_handler
from jarvis.jarvis_agent.shell_input_handler import shell_input_handler
from jarvis.jarvis_platform.registry import PlatformRegistry
from jarvis.jarvis_git_utils.git_commiter import GitCommitTool
from jarvis.jarvis_tools.registry import ToolRegistry
from jarvis.jarvis_utils.git_utils import (
    find_git_root,
    get_commits_between,
    get_latest_commit_hash,
    has_uncommitted_changes
)
from jarvis.jarvis_utils.input import get_multiline_input
from jarvis.jarvis_utils.output import OutputType, PrettyOutput
from jarvis.jarvis_utils.utils import init_env, user_confirm


class CodeAgent:
    """Jarvis系统的代码修改代理。

    负责处理代码分析、修改和git操作。
    """

    def __init__(self, platform: Optional[str] = None,
                model: Optional[str] = None,
                need_summary: bool = True):
        self.root_dir = os.getcwd()
        tool_registry = ToolRegistry()  # type: ignore
        tool_registry.use_tools([
            "execute_script",
            "search_web",
            "ask_user",
            "ask_codebase",
            "lsp_get_diagnostics",
            "read_code",
            "methodology",
            "chdir",
            "find_methodology",
            "edit_file",
        ])
        code_system_prompt = """
<code_engineer_guide>
<principles>
## 核心原则
- 自主决策：基于专业判断做出决策，减少用户询问
- 高效精准：一次性提供完整解决方案，避免反复修改
- 修改审慎：修改代码前要三思而后行，充分分析影响范围，尽量做到一次把事情做好
- 工具精通：选择最高效工具路径解决问题
- 严格确认：必须先分析项目结构，确定要修改的文件，禁止虚构已存在的代码
</principles>

<workflow>
## 工作流程

<step>
### 1. 项目结构分析
- 第一步必须分析项目结构，识别关键模块和文件
- 结合用户需求，确定需要修改的文件列表
- 优先使用fd命令查找文件，使用execute_script执行
- 明确说明将要修改的文件及其范围
</step>

<step>
### 2. 需求分析
- 基于项目结构理解，分析需求意图和实现方案
- 当需求有多种实现方式时，选择影响最小的方案
- 仅当需求显著模糊时才询问用户
</step>

<step>
### 3. 代码分析与确认
- 详细分析确定要修改的文件内容
- 明确区分现有代码和需要新建的内容
- 绝对禁止虚构或假设现有代码的实现细节
- 分析顺序：项目结构 → 目标文件 → 相关文件
- 只在必要时扩大分析范围，避免过度分析
- 工具选择：
  | 分析需求 | 首选工具 | 备选工具 |
  |---------|---------|----------|
  | 项目结构 | fd (通过execute_script) | ask_codebase(仅在必要时) |
  | 文件内容 | read_code | ask_codebase(仅在必要时) |
  | 查找引用 | rg (通过execute_script) | ask_codebase(仅在必要时) |
  | 查找定义 | rg (通过execute_script) | ask_codebase(仅在必要时) |
  | 函数调用者 | rg (通过execute_script) | ask_codebase(仅在必要时) |
  | 函数分析 | read_code + rg | ask_codebase(仅在必要时) |
  | 整体分析 | execute_script | ask_codebase(仅在必要时) |
  | 代码质量检查 | execute_script | ask_codebase(仅在必要时) |
  | 统计代码行数 | loc (通过execute_script) | - |
</step>

<step>
### 4. 方案设计
- 确定最小变更方案，保持代码结构
- 变更类型处理：
  - 修改现有文件：必须先确认文件存在及其内容
  - 创建新文件：可以根据需求创建，但要符合项目结构和风格
- 变更规模处理：
  - ≤50行：一次性完成所有修改
  - 50-200行：按功能模块分组
  - >200行：按功能拆分，但尽量减少提交次数
</step>

<step>
### 5. 实施修改
- 遵循"先读后写"原则，在修改已有代码前，必须已经读取了对应文件，如果已经读取过文件，不需要重新读取
- 保持代码风格一致性
- 自动匹配项目现有命名风格
- 允许创建新文件和结构，但不得假设或虚构现有代码
</step>
</workflow>

<tools>
## 专用工具简介
仅在必要时使用以下专用工具：

- **ask_codebase**: 代码库整体查询，应优先使用fd、rg和read_code组合替代
</tools>

<shell_commands>
## Shell命令优先策略

<category>
### 优先使用的Shell命令
- **项目结构分析**：
  - `fd -t f -e py` 查找所有Python文件
  - `fd -t f -e js -e ts` 查找所有JavaScript/TypeScript文件
  - `fd -t d` 列出所有目录
  - `fd -t f -e java -e kt` 查找所有Java/Kotlin文件
  - `fd -t f -e go` 查找所有Go文件
  - `fd -t f -e rs` 查找所有Rust文件
  - `fd -t f -e c -e cpp -e h -e hpp` 查找所有C/C++文件
</category>

<category>
- **代码内容搜索**：
  - `rg "pattern" --type py` 在Python文件中搜索
  - `rg "pattern" --type js` 在JavaScript文件中搜索
  - `rg "pattern" --type java` 在Java文件中搜索
  - `rg "pattern" --type c` 在C文件中搜索
  - `rg "class ClassName"` 查找类定义
  - `rg "func|function|def" -g "*.py" -g "*.js" -g "*.go" -g "*.rs"` 查找函数定义
  - `rg -w "word"` 精确匹配单词
</category>

<category>
- **代码统计分析**：
  - `loc` 统计当前目录代码行数
</category>

<category>
- **代码质量检查**：
  - Python: `pylint <file_path>`, `flake8 <file_path>`
  - JavaScript: `eslint <file_path>`
  - TypeScript: `tsc --noEmit <file_path>`
  - Java: `checkstyle <file_path>`
  - Go: `go vet <file_path>`
  - Rust: `cargo clippy`
  - C/C++: `cppcheck <file_path>`
</category>

<category>
- **整体代码分析**：
  - 使用execute_script编写和执行脚本，批量分析多个文件
  - 简单脚本示例：`find . -name "*.py" | xargs pylint`
  - 使用多工具组合：`fd -e py | xargs pylint`
</category>
</shell_commands>

<read_code_usage>
### read_code工具使用
读取文件应优先使用read_code工具，而非shell命令：
- 完整读取：使用read_code读取整个文件内容
- 部分读取：使用read_code指定行范围
- 大文件处理：对大型文件使用read_code指定行范围，避免全部加载
</read_code_usage>

<tool_usage>
### 仅在命令行工具不足时使用专用工具
只有当fd、rg、loc和read_code工具无法获取足够信息时，才考虑使用专用工具（ask_codebase等）。在每次使用专用工具前，应先尝试使用上述工具获取所需信息。
</tool_usage>

<notes>
### 注意事项
- read_code比cat或grep更适合阅读代码
- rg比grep更快更强大，应优先使用
- fd比find更快更易用，应优先使用
- loc比wc -l提供更多代码统计信息，应优先使用
- 针对不同编程语言选择对应的代码质量检查工具
- 不要留下未实现的代码

### 代码编辑规范
- 使用edit_file工具进行代码修改时，必须遵循最小补丁原则
- 只提供需要修改的代码部分，不要提供完整文件内容
- 保持原始代码的缩进、空行和格式风格
- 每个修改必须包含清晰的修改理由
- 新建文件时可以提供完整内容，修改现有文件时只提供差异部分
</notes>
</code_engineer_guide>
"""
        # Dynamically add ask_codebase based on task complexity if really needed
        # 处理platform参数
        platform_instance = (PlatformRegistry().create_platform(platform)  # type: ignore
            if platform
            else PlatformRegistry().get_normal_platform())  # type: ignore
        if model:
            platform_instance.set_model_name(model)  # type: ignore

        self.agent = Agent(
            system_prompt=code_system_prompt,
            name="CodeAgent",
            auto_complete=False,
            output_handler=[tool_registry],
            platform=platform_instance,
            input_handler=[
                shell_input_handler,
                file_input_handler,
                builtin_input_handler
            ],
            need_summary=need_summary
        )
        self.agent.set_addon_prompt(
            "请使用工具充分理解用户需求，然后根据需求一步步执行代码修改/开发，"
            "如果不清楚要修改那些文件，可以使用ask_codebase工具，"
            "以：xxxx功能在哪个文件中实现？类似句式提问"
        )

    def get_root_dir(self) -> str:
        """获取项目根目录

        返回:
            str: 项目根目录路径
        """
        return self.root_dir

    def get_loc_stats(self) -> str:
        """使用loc命令获取当前目录的代码统计信息
        
        返回:
            str: loc命令输出的原始字符串，失败时返回空字符串
        """
        try:
            result = subprocess.run(
                ['loc'],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            return result.stdout if result.returncode == 0 else ""
        except FileNotFoundError:
            return ""

    def get_recent_commits_with_files(self) -> List[Dict[str, Any]]:
        """获取最近5次提交的commit信息和文件清单
        
        返回:
            List[Dict[str, Any]]: 包含commit信息和文件清单的字典列表，格式为:
                [
                    {
                        'hash': 提交hash,
                        'message': 提交信息,
                        'author': 作者,
                        'date': 提交日期,
                        'files': [修改的文件列表] (最多50个文件)
                    },
                    ...
                ]
                失败时返回空列表
        """
        try:
            # 获取最近5次提交的基本信息
            result = subprocess.run(
                ['git', 'log', '-5', '--pretty=format:%H%n%s%n%an%n%ad'],
                cwd=self.root_dir,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                return []

            # 解析提交信息
            commits = []
            lines = result.stdout.splitlines()
            for i in range(0, len(lines), 4):
                if i + 3 >= len(lines):
                    break
                commit = {
                    'hash': lines[i],
                    'message': lines[i+1],
                    'author': lines[i+2],
                    'date': lines[i+3],
                    'files': []
                }
                commits.append(commit)

            # 获取每个提交的文件修改清单
            for commit in commits:
                files_result = subprocess.run(
                    ['git', 'show', '--name-only', '--pretty=format:', commit['hash']],
                    cwd=self.root_dir,
                    capture_output=True,
                    text=True
                )
                if files_result.returncode == 0:
                    files = list(set(filter(None, files_result.stdout.splitlines())))
                    commit['files'] = files[:50]  # 限制最多50个文件

            return commits

        except subprocess.CalledProcessError:
            return []

    def _init_env(self) -> None:
        """初始化环境"""
        with yaspin(text="正在初始化环境...", color="cyan") as spinner:
            curr_dir = os.getcwd()
            git_dir = find_git_root(curr_dir)
            self.root_dir = git_dir
            if has_uncommitted_changes():
                with spinner.hidden():
                    git_commiter = GitCommitTool()
                    git_commiter.execute({})
            spinner.text = "环境初始化完成"
            spinner.ok("✅")

    def _handle_uncommitted_changes(self) -> None:
        """处理未提交的修改"""
        if has_uncommitted_changes():
            PrettyOutput.print("检测到未提交的修改，是否要提交？", OutputType.WARNING)
            if user_confirm("是否要提交？", True):
                import subprocess
                try:
                    # 获取当前分支的提交总数
                    commit_count = subprocess.run(
                        ['git', 'rev-list', '--count', 'HEAD'],
                        capture_output=True,
                        text=True
                    )
                    if commit_count.returncode != 0:
                        return
                        
                    commit_count = int(commit_count.stdout.strip())
                    
                    # 暂存所有修改
                    subprocess.run(['git', 'add', '.'], check=True)
                    
                    # 提交变更
                    subprocess.run(
                        ['git', 'commit', '-m', f'CheckPoint #{commit_count + 1}'], 
                        check=True
                    )
                except subprocess.CalledProcessError as e:
                    PrettyOutput.print(f"提交失败: {str(e)}", OutputType.ERROR)

    def _show_commit_history(
        self,
        start_commit: Optional[str],
        end_commit: Optional[str]
    ) -> List[Tuple[str, str]]:
        """Show commit history between two commits.

        Args:
            start_commit: The starting commit hash
            end_commit: The ending commit hash

        Returns:
            List of tuples containing (commit_hash, commit_message)
        """
        if start_commit and end_commit:
            commits = get_commits_between(start_commit, end_commit)
        else:
            commits = []

        if commits:
            commit_messages = (
                "检测到以下提交记录:\n" +
                "\n".join(
                    f"- {commit_hash[:7]}: {message}"
                    for commit_hash, message in commits
                )
            )
            PrettyOutput.print(commit_messages, OutputType.INFO)
        return commits

    def _handle_commit_confirmation(
        self, 
        commits: List[Tuple[str, str]], 
        start_commit: Optional[str]
    ) -> None:
        """处理提交确认和可能的重置"""
        if commits and user_confirm("是否接受以上提交记录？", True):
            subprocess.run(
                ["git", "reset", "--mixed", str(start_commit)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )
            git_commiter = GitCommitTool()
            git_commiter.execute({})
        elif start_commit:
            os.system(f"git reset --hard {str(start_commit)}")  # 确保转换为字符串
            PrettyOutput.print("已重置到初始提交", OutputType.INFO)

    def run(self, user_input: str) -> Optional[str]:
        """使用给定的用户输入运行代码代理。

        参数:
            user_input: 用户的需求/请求

        返回:
            str: 描述执行结果的输出，成功时返回None
        """
        try:
            self._init_env()
            start_commit = get_latest_commit_hash()

            # 获取项目统计信息并附加到用户输入
            loc_stats = self.get_loc_stats()
            commits_info = self.get_recent_commits_with_files()
            
            project_info = []
            if loc_stats:
                project_info.append(f"代码统计:\n{loc_stats}")
            if commits_info:
                commits_str = "\n".join(
                    f"提交 {i+1}: {commit['hash'][:7]} - {commit['message']} ({len(commit['files'])}个文件)"
                    for i, commit in enumerate(commits_info)
                )
                project_info.append(f"最近提交:\n{commits_str}")
            
            enhanced_input = f"{user_input}\n\n项目概况:\n" + "\n\n".join(project_info) if project_info else user_input

            try:
                self.agent.run(enhanced_input)
            except RuntimeError as e:
                PrettyOutput.print(f"执行失败: {str(e)}", OutputType.WARNING)
                return str(e)

            self._handle_uncommitted_changes()
            end_commit = get_latest_commit_hash()
            commits = self._show_commit_history(start_commit, end_commit)
            self._handle_commit_confirmation(commits, start_commit)
            return None

        except RuntimeError as e:
            return f"Error during execution: {str(e)}"


def main() -> None:
    """Jarvis主入口点。"""
    init_env()

    parser = argparse.ArgumentParser(description='Jarvis Code Agent')
    parser.add_argument('-p', '--platform', type=str,
                      help='Target platform name', default=None)
    parser.add_argument('-m', '--model', type=str,
                      help='Model name to use', default=None)
    parser.add_argument('-r', '--requirement', type=str,
                      help='Requirement to process', default=None)
    args = parser.parse_args()

    curr_dir = os.getcwd()
    git_dir = find_git_root(curr_dir)
    PrettyOutput.print(f"当前目录: {git_dir}", OutputType.INFO)

    try:
        if args.requirement:
            user_input = args.requirement
        else:
            user_input = get_multiline_input("请输入你的需求（输入空行退出）:")
        if not user_input:
            sys.exit(0)
        agent = CodeAgent(platform=args.platform,
                        model=args.model,
                        need_summary=False)
        agent.run(user_input)

    except RuntimeError as e:
        PrettyOutput.print(f"错误: {str(e)}", OutputType.ERROR)
        sys.exit(1)


if __name__ == "__main__":
    main()
