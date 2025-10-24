## Security Policy

### Supported Versions

We provide security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| latest  | ✅ Yes             |
| 1.x.x   | ✅ Yes             |

### Reporting a Vulnerability

If you discover a security vulnerability, please report it by emailing the maintainers privately. Please do not create a public GitHub issue for security vulnerabilities.

**Please include the following information in your report:**

1. Description of the vulnerability
2. Steps to reproduce the vulnerability
3. Potential impact of the vulnerability
4. Any suggested fixes or mitigations

We will acknowledge receipt of your vulnerability report within 48 hours and will send you regular updates about our progress. If the vulnerability is accepted, we will:

1. Work on a fix in a private repository
2. Prepare a security advisory
3. Release a patched version
4. Publicly disclose the vulnerability after the fix is available

### Security Considerations

This project handles SNMP communications with network devices. Please consider the following security aspects:

#### SNMP Community Strings
- Use strong, unique community strings
- Avoid default community strings like "public"
- Consider using SNMP v3 with authentication if your Ruckus APs support it

#### Network Security
- Deploy the exporter in a secure network segment
- Use firewalls to restrict access to the metrics endpoint
- Consider using TLS termination via a reverse proxy

#### Container Security
- The container runs as a non-root user for security
- Regular security scans are performed on the base images
- Keep Docker and base images updated

#### Metrics Endpoint
- The metrics endpoint may expose network topology information
- Restrict access to authorized monitoring systems only
- Consider authentication/authorization for production deployments

### Security Features

- **Non-root container**: Runs as dedicated user account
- **Minimal attack surface**: Only necessary dependencies included
- **Health checks**: Built-in monitoring for container health
- **Logging**: Comprehensive logging for security monitoring

### Responsible Disclosure

We follow responsible disclosure practices and ask that security researchers do the same. We appreciate your efforts to help keep this project secure!