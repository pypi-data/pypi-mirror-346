# Dog Eye Diagnosis MCP Server

[ENG](#english) | [KOR](#한국어)

---

## English

This package provides a Model Context Protocol (MCP) server for analyzing dog's eye images and returning probabilities for 10 different diseases.

### Installation

Install the package from PyPI using UV or pip:

```bash
uv pip install dog-eye-diagnosis-mcp-server
```

or

```bash
pip install dog-eye-diagnosis-mcp-server
```

### Configuration

Configure your MCP server by adding the following entry to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dog_eye_diagnosis": {
      "command": "uvx",
      "args": [
        "dog-eye-diagnosis-mcp-server"
      ]
    }
  }
}
```

### Usage

Ensure the server is properly installed and configured, then run your MCP setup or restart your application to enable the Dog Eye Diagnosis MCP server.

### License

MIT

---

## 한국어

이 패키지는 강아지의 눈 이미지를 분석하여 10가지 질병에 대한 확률을 반환하는 MCP(Model Context Protocol) 서버를 제공합니다.

### 설치 방법

UV 또는 pip를 이용하여 PyPI에서 패키지를 설치합니다:

```bash
uv pip install dog-eye-diagnosis-mcp-server
```

또는

```bash
pip install dog-eye-diagnosis-mcp-server
```

### 설정 방법

MCP 서버를 사용하기 위해 `claude_desktop_config.json` 파일에 다음 내용을 추가합니다:

```json
{
  "mcpServers": {
    "dog_eye_diagnosis": {
      "command": "uvx",
      "args": [
        "dog-eye-diagnosis-mcp-server"
      ]
    }
  }
}
```

### 사용 방법

설치를 완료하고 위 설정을 적용한 후 MCP 설정을 실행하거나 애플리케이션을 재시작하여 Dog Eye Diagnosis MCP 서버를 활성화하세요.

### 라이센스

MIT
