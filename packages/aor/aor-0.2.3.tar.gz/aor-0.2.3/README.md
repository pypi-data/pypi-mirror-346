# AI on Rails

[![PyPI version](https://img.shields.io/pypi/v/aor.svg)](https://pypi.org/project/aor/)

`AI on Rails` is a marketplace for AI Agents that provide commercial services to wide audiences.
`aor` is a Python module provided by `AI on Rails` to manage AI Agent listings on the marketplace,
and to speed up creating AI Agents locally, deploying them to the infrastructure of your choice,
and publishing to `AI on Rails`.
Together, the marketplace and this Python package provide the shortest well lit path from an idea to monetization.

Advanced users are expected to develop AI Agents using comprehensive third-party tools and
frameworks, and use the `aor` Python package to publish the marketplace listings only.
However `AI on Rails` will continue developing builtin templates to extend the list of
supported frameworks and technologies, to give the beginner users a wider list of options available
to bootstrap their AI Agents without putting proprietary information (such as prompts!)
at risk of being exposed to third parties such as tool providers.

> **IMPORTANT: ALPHA VERSION**  
> AI-on-Rails is currently in alpha status. The API and features are subject to change without notice. Use in production environments at your own risk. We welcome feedback and bug reports to help improve the framework.

## Installation

```bash
# Install the AI-on-Rails command line tools
$ pip install -U aor
$ aor --help
$ aor login
```

### Prerequisites

- **Python**: Version 3.10 or higher
- **AWS CLI**: Configured with appropriate credentials (for AWS deployments)
- **SAM CLI**: AWS Serverless Application Model CLI (for AWS Lambda deployments)
- **Docker**: For local testing and deployment packaging (optional)

### Environment Setup

Depending on desired components and features, additional environment variables need to be set:

```bash
# AWS credentials (if deploying to AWS)
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=your_preferred_region
```

## User's Guide

### Create a Basic Application

In AI-on-Rails, one or more AI Agents are bundled into an application which is advertised and sold to users.
Create a new AI-on-Rails application with the basic directory structure and configuration files:

```bash
aor new my-first-app
cd my-first-app
```

### Application Creation Options

A few things can be customized at the moment the application is created:

```bash
# Create an application with a description
aor new my-first-app --desc "<Why would someone use/buy this application?>"

# Create an application with tags to make it discoverable
aor new my-first-app --tag "<Industry>" --tag "<Business Function>" --tag "<Audience>"

# Create an application to be displayed for audience using certain language
aor new my-first-app --lang en

# Create an application with pricing options
aor new my-first-app --currency USD --buy-price 299.99 --rent-price 9.99 --rent-period 7 --query-price 0.09
```

Available options:
- `--desc`: Description of the application
- `--tag`: Tag for the application (can be used multiple times)
- `--lang`: Language of the application (default: en)
- `--currency`: Currency used for pricing (default: USD)
- `--buy-price`: Price to purchase the application indefinitely
- `--rent-price`: Price to rent the application for a period of time
- `--rent-period`: Period of time to rent the application (in days)
- `--query-price`: Price per query

### Add an AI Agent

Each application can contain one or more AI Agents:

```bash
aor add my-conversation-agent --type langgraph --protocol a2a
```

### Customize AI Agent

Now comes the most important part, where you do what really matters:
edit prompts and logic in the generated AI Agent.

```bash
$ ls src/my-conversation-agent
...
prompts.py
nodes.py
...
```

### Deploy to Your Infrastructure

Later, a range of deployment options will be available for your private workloads.
For now, only deployment to your AWS Account is supported:

```bash
# Add AWS Lambda deployment configuration
aor add my-conversation-agent --deploy aws-lambda

# Deploy
aor deploy
```

Now your AI Agent is online.
But the users don't know where to find it.
It's not a complete usable product because it's missing the whole UI/UX layer:
multiplatform client software, billing, user data persistence, etc.

### Publish to AI-on-Rails

Make you AI Agent available for commercial use worldwide:

```bash
# Login to AI-on-Rails
aor login

# Publish your agent
aor publish
```

### Send a Request to Your Published Endpoint

```bash
# Send a request to your published agent
aor execute --input query "<A question users may ask when they seek business expertise on the topic you master>"
```

## Configuration

All application and AI Agent details are persisted in the ``aionrails.yaml`` file.
Feel free to make changes manually and verify the with ``aor lint``.

```yaml
name: my-application
desc: My AI application
version: 0.1.0
cover: ./data/images/logo.png

endpoints:
  - name: my-agent
    desc: A conversational agent
    protocol: rest
    type: langgraph
    path: my_agent.py
    input:
      - name: query
        type: text
        desc: The input query
    output:
      - name: response
        type: text
        desc: The agent's response
```

