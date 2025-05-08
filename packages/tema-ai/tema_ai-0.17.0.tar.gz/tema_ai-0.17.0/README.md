<p align="center">
 <img width="300px" src="https://github.com/tema-ai/.github/blob/production/profile/images/WorldLoop.gif?raw=true" align="center" alt="GitHub Readme Stats" />
 <h2 align="center">Tema AI</h2>
 <p align="center">A library to connect to Tema AI data</p>
</p>


<p align="center">
  <img src="https://img.shields.io/badge/python-3.8|3.9|3.10|3.11|3.12-navy.svg" />
  <a href="https://codeclimate.com/repos/66c8e6bbf971e32db3aa5473/maintainability">
    <img src="https://api.codeclimate.com/v1/badges/7f59c6625078be938fff/maintainability">
  </a>
  <a href="https://codeclimate.com/repos/66c8e6bbf971e32db3aa5473/test_coverage">
    <img src="https://api.codeclimate.com/v1/badges/7f59c6625078be938fff/test_coverage">
  </a>
</p>
<p align="center">
  <a href="https://github.com/tema-ai/tema_ai_connect/actions/workflows/black.yml">
    <img alt="Black" src="https://github.com/tema-ai/tema_ai_connect/actions/workflows/black.yml/badge.svg" />
  </a>
  <a href="https://github.com/tema-ai/tema_ai_connect/actions/workflows/publish-to-pypi.yml">
    <img alt="release" src="https://github.com/tema-ai/tema_ai_connect/actions/workflows/publish-to-pypi.yml/badge.svg?event=release"/>
  </a>
  <a href="https://github.com/tema-ai/tema_ai_connect/actions/workflows/mypy.yml">
    <img alt="typing" src="https://github.com/tema-ai/tema_ai_connect/actions/workflows/mypy.yml/badge.svg"/>
  </a>
</p>

### Setting up the connection

You will need access to Tema AI API in order to use this library. Please generate the appropriate API client id and secret as well as the connection. Once you have those 3 values in addition to the sharing host you can configure the library to connect to the systems. Refer to the provided documentation to know how to generate those values if you don't already have them. Test

### Setting up the environment

You have two options to provide the access variables:

1. Provide them as environment variables and the code will automatically pick them up.

    ```bash
    export TEMA_AI_CONNECTION=connector_name
    export TEMA_AI_HOST=https://provided-host.ai
    export TEMA_AI_CLIENT_ID=HCD35....HAm34
    export TEMA_AI_CLIENT_SECRET=n...ryA
    ```

    or provide them in an environment file

    ```bash
    #.env

    TEMA_AI_CONNECTION=connector_name
    TEMA_AI_HOST=https://provided-host.ai
    TEMA_AI_CLIENT_ID=HCD35....HAm34
    TEMA_AI_CLIENT_SECRET=n...ryA
    ```

    ```python
    from tema_ai.connect import TemaAIShareAPI

    connection = TemaAIShareAPI()
    ```

2. Or simply provide them on runtime

    ```python
    from tema_ai.connect import TemaAIShareAPI

    connection = TemaAIShareAPI(
        connection_name="connector_name",
        host="https://provided-host.ai",
        client_id="HCD35....HAm34"
        client_secret="n...ryA"
    )

    ```

3. Alternatively you can mix and match and provide some of the variables through the environment and some directly to the class.
