# 认证授权API

## 认证机制

我们的API使用Bearer Token进行认证。每个请求都需要在Header中包含认证Token：
```
Authorization: Bearer <your_token>
```

## 获取Token

1. 用户注册后，系统会生成一个唯一的API Token。
2. 用户可以通过登录接口获取Token。
3. Token需要妥善保管，不要泄露给他人。

## Token刷新

- Token有一定的有效期，过期后需要重新获取。
- 用户可以通过刷新Token接口获取新的Token。

## 授权流程

1. 用户在登录后获取Token。
2. 在每次请求API时，附带Token进行认证。
3. 系统验证Token的有效性，允许或拒绝请求。

## 错误处理

- 401: 未认证，Token无效或缺失。
- 403: 未授权，用户没有访问资源的权限。

错误响应格式：
```json
{
    "status": "error",
    "detail": "错误描述"
}
```

## 注意事项

1. 确保Token的安全性，不要在客户端代码中硬编码Token。
2. 定期更新Token，确保其有效性。
3. 如果发现Token泄露，请立即重置Token。 