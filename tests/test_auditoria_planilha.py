"""Testes automatizados com pytest para validar o simulador e a estrutura da planilha."""

from pathlib import Path
import pytest

from src.simulador_financeiro import ParametrosNegocio, comparar_cenarios, simular_cenario


@pytest.fixture
def parametros_padrao() -> ParametrosNegocio:
    """Fornece parâmetros base consistentes para os testes."""
    return ParametrosNegocio(
        investimento_inicial=120000.00,
        custos_fixos_mensais=28000.00,
        preco_medio_unidade=65.00,
        custo_variavel_unidade=23.00,
        margem_liquida_alvo=0.20,
    )


def test_margem_e_ponto_equilibrio(parametros_padrao: ParametrosNegocio) -> None:
    """Valida margem de contribuição e ponto de equilíbrio mensal."""
    assert parametros_padrao.margem_contribuicao_unitaria == pytest.approx(42.00)
    assert parametros_padrao.margem_contribuicao_percentual == pytest.approx(42.00 / 65.00)
    assert parametros_padrao.ponto_equilibrio_unidades == pytest.approx(28000.00 / 42.00)
    assert parametros_padrao.ponto_equilibrio_receita == pytest.approx(
        (28000.00 / 42.00) * 65.00
    )


def test_simulacao_cenario_positivo(parametros_padrao: ParametrosNegocio) -> None:
    """Verifica cálculo de receita, custos, lucro operacional e payback."""
    resultado = simular_cenario(parametros_padrao, 1000)

    assert resultado["receita_mensal"] == 65000.00
    assert resultado["custos_variaveis_mensais"] == 23000.00
    assert resultado["custos_totais_mensais"] == 51000.00
    assert resultado["resultado_operacional"] == 14000.00
    assert resultado["lucro_liquido_estimado"] == 13000.00
    assert resultado["payback_meses"] == pytest.approx(120000.00 / 13000.00, abs=0.01)


def test_comparacao_multiplos_cenarios(parametros_padrao: ParametrosNegocio) -> None:
    """Confirma que múltiplos volumes retornam resultados na mesma ordem."""
    cenarios = comparar_cenarios(parametros_padrao, [500, 1000])
    assert len(cenarios) == 2
    assert cenarios[0]["resultado_operacional"] < cenarios[1]["resultado_operacional"]


def test_volume_negativo_levanta_erro(parametros_padrao: ParametrosNegocio) -> None:
    """Garante que volumes mensais negativos não sejam aceites."""
    with pytest.raises(ValueError):
        simular_cenario(parametros_padrao, -10)


def test_arquivo_planilha_existe() -> None:
    """Verifica se o ficheiro Excel do modelo de negócio está presente em data/."""
    caminho_planilha = Path("data/modelo_negocio_pizzaria.xlsx")
    assert caminho_planilha.exists()
