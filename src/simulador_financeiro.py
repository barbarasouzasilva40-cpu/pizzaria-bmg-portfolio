Python
"""Simulador financeiro e de cenários para modelo BMG Canvas de pizzaria."""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class ParametrosNegocio:
    """Parâmetros financeiros base do modelo de negócio."""

    investimento_inicial: float
    custos_fixos_mensais: float
    preco_medio_unidade: float
    custo_variavel_unidade: float
    margem_liquida_alvo: float = 0.20

    @property
    def margem_contribuicao_unitaria(self) -> float:
        """Retorna quanto cada unidade vendida contribui para cobrir custos fixos."""
        return self.preco_medio_unidade - self.custo_variavel_unidade

    @property
    def margem_contribuicao_percentual(self) -> float:
        """Retorna a margem de contribuição unitária em percentual do preço."""
        if self.preco_medio_unidade <= 0:
            return 0.0
        return self.margem_contribuicao_unitaria / self.preco_medio_unidade

    @property
    def ponto_equilibrio_unidades(self) -> float:
        """Retorna a quantidade mensal de unidades para empatar receitas e custos."""
        if self.margem_contribuicao_unitaria <= 0:
            raise ValueError("A margem de contribuição unitária deve ser maior que zero.")
        return self.custos_fixos_mensais / self.margem_contribuicao_unitaria

    @property
    def ponto_equilibrio_receita(self) -> float:
        """Retorna o faturamento mensal necessário para atingir o ponto de equilíbrio."""
        return self.ponto_equilibrio_unidades * self.preco_medio_unidade


def simular_cenario(parametros: ParametrosNegocio, unidades_mes: int) -> Dict[str, float]:
    """Simula receita, custos, lucro operacional e payback para um volume mensal."""
    if unidades_mes < 0:
        raise ValueError("A quantidade de unidades mensais não pode ser negativa.")

    receita_mensal = unidades_mes * parametros.preco_medio_unidade
    custos_variaveis_mensais = unidades_mes * parametros.custo_variavel_unidade
    custos_totais_mensais = parametros.custos_fixos_mensais + custos_variaveis_mensais
    resultado_operacional = receita_mensal - custos_totais_mensais
    lucro_liquido_estimado = receita_mensal * parametros.margem_liquida_alvo

    if lucro_liquido_estimado > 0:
        payback_meses = parametros.investimento_inicial / lucro_liquido_estimado
    else:
        payback_meses = float("inf")

    return {
        "unidades_mes": float(unidades_mes),
        "receita_mensal": round(receita_mensal, 2),
        "custos_variaveis_mensais": round(custos_variaveis_mensais, 2),
        "custos_totais_mensais": round(custos_totais_mensais, 2),
        "resultado_operacional": round(resultado_operacional, 2),
        "lucro_liquido_estimado": round(lucro_liquido_estimado, 2),
        "payback_meses": round(payback_meses, 2) if payback_meses != float("inf") else float("inf"),
    }


def comparar_cenarios(
    parametros: ParametrosNegocio, volumes_mensais: List[int]
) -> List[Dict[str, float]]:
    """Executa a simulação financeira para uma lista de volumes mensais."""
    return [simular_cenario(parametros, volume) for volume in volumes_mensais]


if __name__ == "__main__":
    modelo_base = ParametrosNegocio(
        investimento_inicial=120000.00,
        custos_fixos_mensais=28000.00,
        preco_medio_unidade=65.00,
        custo_variavel_unidade=23.00,
        margem_liquida_alvo=0.20,
    )

    print(f"Margem de contribuição unitária: R$ {modelo_base.margem_contribuicao_unitaria:.2f}")
    print(f"Margem de contribuição (%): {modelo_base.margem_contribuicao_percentual * 100:.1f}%")
    print(f"Ponto de equilíbrio (unidades/mês): {modelo_base.ponto_equilibrio_unidades:.1f}")
    print(f"Ponto de equilíbrio (receita/mês): R$ {modelo_base.ponto_equilibrio_receita:.2f}\n")

    for cenario in comparar_cenarios(modelo_base, [600, 800, 1000, 1200]):
        print(cenario)
