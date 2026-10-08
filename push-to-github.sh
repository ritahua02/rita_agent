#!/usr/bin/env bash
#
# 将 Rita 项目推送到 GitHub
# 目标仓库：https://github.com/ritahua02/rita_agent
#
# 前置条件：
#   1. 已安装 git（macOS: xcode-select --install 或 brew install git）
#   2. 已完成 GitHub 身份认证（HTTPS 用 Personal Access Token，或已配置 SSH key）
#
# 用法：在项目根目录执行  bash push-to-github.sh
#

set -euo pipefail

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

REMOTE_URL="https://github.com/ritahua02/rita_agent.git"
BRANCH="main"

log()  { printf "\033[1;36m[push]\033[0m %s\n" "$1"; }
err()  { printf "\033[1;31m[error]\033[0m %s\n" "$1" >&2; }

if ! command -v git >/dev/null 2>&1; then
  err "未找到 git。请先安装：macOS 执行  xcode-select --install  或  brew install git"
  exit 1
fi

# 初始化仓库（若尚未初始化）
if [ ! -d .git ]; then
  git init
  log "已初始化 git 仓库"
fi

# 确保在 main 分支
git checkout -B "${BRANCH}"

# 配置远程
if git remote | grep -q "^origin$"; then
  git remote set-url origin "${REMOTE_URL}"
  log "已更新 origin 远程地址"
else
  git remote add origin "${REMOTE_URL}"
  log "已添加 origin 远程地址"
fi

# 暂存并提交
git add -A
if git diff --cached --quiet; then
  log "没有需要提交的变更"
else
  git commit -m "chore: initial public release (sanitized)"
  log "已创建提交"
fi

# 推送
log "推送到 ${REMOTE_URL} (${BRANCH}) ..."
git push -u origin "${BRANCH}"

log "完成 ✅  仓库地址：https://github.com/ritahua02/rita_agent"
