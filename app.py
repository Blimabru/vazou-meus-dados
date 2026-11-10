"""Ponto de entrada mínimo da aplicação Streamlit.

O fluxo da interface fica em ``src.main`` para manter este arquivo simples e
compatível com o comando ``streamlit run app.py``.
"""

from src.main import main


if __name__ == "__main__":
    # Executa a aplicação somente quando este arquivo é iniciado diretamente.
    # O condicional evita efeitos colaterais quando o módulo é importado por
    # testes, ferramentas de análise ou pelo próprio Streamlit.
    main()
