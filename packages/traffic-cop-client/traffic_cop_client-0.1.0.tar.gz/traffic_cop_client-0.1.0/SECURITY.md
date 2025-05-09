# Security Policy

## Supported Versions

We currently support the following versions of the Traffic Cop Python SDK with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |
| < 0.1.0 | :x:                |

## Reporting a Vulnerability

We take the security of the Traffic Cop Python SDK seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email us at security@trafficcop.ai** with details about the vulnerability
3. Include the following information in your report:
   - Type of vulnerability
   - Full path to the vulnerable file(s)
   - Steps to reproduce
   - Potential impact
   - Any potential fixes (if you have suggestions)

## What to Expect

- We will acknowledge receipt of your vulnerability report within 48 hours
- We will provide a more detailed response within 7 days, indicating the next steps in handling your report
- We will keep you informed of our progress as we work to address the vulnerability
- We will notify you when the vulnerability is fixed

## Security Best Practices for Users

When using the Traffic Cop Python SDK, we recommend the following security best practices:

1. **Keep the SDK updated**: Always use the latest version to benefit from security patches
2. **Secure your API keys**: Never hardcode API keys in your application code or commit them to version control
3. **Use environment variables**: Store sensitive information like API keys in environment variables
4. **Enable SSL verification**: Only disable SSL verification in development environments when absolutely necessary
5. **Implement proper error handling**: Catch and handle exceptions appropriately to prevent information leakage

## Dependency Security

The Traffic Cop Python SDK has minimal dependencies to reduce the attack surface. We regularly monitor our dependencies for security vulnerabilities and update them as needed.
