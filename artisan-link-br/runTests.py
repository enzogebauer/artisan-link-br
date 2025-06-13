#!/usr/bin/env python3
"""
Script para executar os testes seguindo TDD
"""
import subprocess
import sys


def run_tests():
    """Execute os testes com pytest"""
    try:
        # Executar testes com coverage
        result = subprocess.run(
            [
                "python3",
                "-m",
                "pytest",
                "tests/",
                "-v",
                "--cov=core",
                "--cov=adapters",
                "--cov-report=html",
                "--cov-report=term-missing",
            ],
            check=True,
        )

        print("\n✅ Todos os testes passaram!")
        print("📊 Relatório de cobertura gerado em htmlcov/index.html")

    except subprocess.CalledProcessError as e:
        print(f"\n❌ Alguns testes falharam (código de saída: {e.returncode})")
        print(
            "🔧 Isso é esperado no TDD - implemente o código para fazer os testes passarem!"
        )
        sys.exit(1)
    except FileNotFoundError:
        print("❌ pytest não encontrado. Instale com: pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
