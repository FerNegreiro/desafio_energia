# Modelagem Preditiva de Preços Futuros de Energia

Este projeto apresenta uma solução de modelagem preditiva para os preços de energia no mercado futuro brasileiro (ACL), com foco em avaliar o impacto do Custo Marginal de Operação (CMO) do Newave como variável preditora.

## 📄 O Problema

O mercado de energia livre (ACL) é caracterizado pela alta volatilidade e incerteza nos preços futuros. Para empresas que atuam neste mercado (geradoras, comercializadoras e grandes consumidores), essa incerteza representa um risco financeiro significativo, dificultando o planejamento de longo prazo e a negociação de contratos.

A tomada de decisão baseada apenas em dados históricos de preços é limitada, pois não incorpora informações técnicas e fundamentais sobre as condições do sistema elétrico, como a previsão de chuvas e o nível dos reservatórios, que são consolidadas no CMO calculado pelo Newave.

## 💡 A Solução Proposta

Para endereçar este problema, foi desenvolvido um pipeline de modelagem em Python que compara duas abordagens de forma sistemática:

1.  **Modelo Baseline (SARIMA):** Um modelo de série temporal que utiliza exclusivamente o histórico de preços para estabelecer uma performance de referência.
2.  **Modelo Enriquecido (SARIMAX):** Um modelo que incorpora o Custo Marginal de Operação (CMO) do Newave como uma variável exógena, testando a hipótese de que essa informação melhora a acurácia das previsões.

A solução é estruturada em módulos, permitindo a fácil extensão para novas fontes de dados e modelos, e automatiza todo o processo de treino, teste e avaliação de performance.

## 🚀 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/FerNegreiro/desafio_energia.git
    cd desafio_energia
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv .venv
    # Windows
    .\.venv\Scripts\activate
    # macOS / Linux
    source .venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute o pipeline principal:**
    ```bash
    python main.py
    ```

## 🏗️ Estrutura do Projeto

-   `main.py`: Orquestrador principal que executa todo o fluxo de modelagem.
-   `gerar_dados.py`: Script para gerar dados sintéticos para fins de teste.
-   `loaders/`: Módulos para carregamento e pré-processamento de dados.
-   `predictor/`: Módulos com as classes dos modelos preditivos.
-   `data/`: Diretório para armazenamento dos dados.
-   `requirements.txt`: Lista de dependências do projeto.
