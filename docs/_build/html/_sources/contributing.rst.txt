Contribution Guidelines
=======================

How to Contribute
-----------------
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure code passes all checks:

   .. code-block:: bash

      poetry run black .
      poetry run flake8
      poetry run pytest

5. Submit a pull request

Coding Standards
----------------
- Follow PEP8 guidelines
- Use Google-style docstrings
- Type hints for all public functions
- 100% test coverage for new features

Security Practices
------------------
- Scan dependencies for vulnerabilities before upgrading
- Never include secrets in code/docker images
- Follow container security guidelines from installation docs
- Report vulnerabilities via SECURITY.md process
- Review Dockerfile changes for security implications

Documentation
-------------
- Update relevant documentation when making API changes
- Add examples for new features
- Keep docstrings consistent with existing style

Issue Reporting
---------------
- Use GitHub Issues template
- Include reproduction steps
- Specify Python and package versions