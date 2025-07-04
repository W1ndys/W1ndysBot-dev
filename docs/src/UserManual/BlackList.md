---
title: 黑名单系统
---

# 黑名单系统

支持群组级和全局级黑名单管理，检测用户入群或发言时是否在黑名单中，如果检测到黑名单用户，会自动撤回消息并踢出，黑名单用户不再接受入群。

## 命令

### 模块开关
- `BL` 开关黑名单系统

### 群组黑名单管理
- `拉黑` 添加黑名单，支持at和纯QQ号，例如：拉黑[CQ:at,qq=1234567890] 或 拉黑 1234567890，支持多个QQ号，例如：拉黑[CQ:at,qq=1234567890] [CQ:at,qq=1234567890] 或 拉黑 1234567890 1234567890
- `解黑` 移除黑名单，使用方法同拉黑命令
- `看黑` 查看当前群组黑名单
- `清黑` 清空当前群组黑名单

### 全局黑名单管理
- `全局拉黑` 添加全局黑名单，使用方法同拉黑命令
- `全局解黑` 移除全局黑名单，使用方法同解黑命令
- `全局看黑` 查看全局黑名单
- `全局清黑` 清空全局黑名单

## 使用示例

```
# 拉黑单个用户
拉黑 1234567890
拉黑 [CQ:at,qq=1234567890]

# 批量拉黑
拉黑 1234567890 1234567891 1234567892
拉黑 [CQ:at,qq=1234567890] [CQ:at,qq=1234567891]

# 全局拉黑
全局拉黑 1234567890
```

## 示例图片

> 暂时空着
