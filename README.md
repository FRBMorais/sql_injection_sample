
# 🛡️ Relatório de Vulnerabilidade

## 1. Resumo

- **Título**: _SQL Injection crítico no Apache Traffic Control (CVE‑2024‑45387)_
- **Data do Relato**: `23 de dezembro de 2024`
- **Relator/Descoberto por**: Felipe Rosa / Tencent YunDing Security Lab
- **Sistema/Aplicativo Alvo**: Apache Traffic Control – componente Traffic Ops (versões 8.0.0 e 8.0.1)
- **Ambiente**: Produção (serviços CDN)

---

### 1.1 Resumo Executivo

Em dezembro de 2024, foi descoberta uma falha de **SQL Injection** em Traffic Ops, interface RESTful do Apache Traffic Control. A falha permitia que usuários privilegiados com `role` (`admin`, `federation`, `operations`, `portal` or `steeting`) executassem comandos SQL arbitrários via requisições PUT especialmente criadas ([thehackernews.com](https://thehackernews.com/2024/12/critical-sql-injection-vulnerability-in.html)). A vulnerabilidade foi classificada com **CVSS 9.9** pelo Apache e **8.8** pela NVD.

---

## 2. Detalhes da Vulnerabilidade

- **Tipo de Vulnerabilidade**: `SQL Injection`
- **CWE**: `CWE‑89: Improper Neutralization of Special Elements used in an SQL Command`
- **Pontuação CVSS**:  
  - Apache CMS (CNA): 9.9 CRITICAL
  - NVD: 8.8 HIGH
- **Componentes Afetados**: `Traffic Ops API`, endpoint PUT `/api/.../deliveryservice_request_comments`
- **Versões Vulneráveis**: >= 8.0.0 & <= 8.0.1
- **Versão com correção**: 8.0.2

---

## 3. Impacto

- **Confidencialidade**: Alta – possível vazamento de dados sensíveis do banco
- **Integridade**: Permite alteração/manipulação de dados
- **Disponibilidade**: Alta – risco de interrupção via comandos maliciosos
- **Escopo**: Restringido a usuários com roles privilegiados (`admin`, `operations`, etc.)

---

## 4. Técnicas de Exploração

- A falha é explorada enviando HTTP PUT maliciosas com payloads no corpo, causando injeções SQL.
- Exemplos indicam exploração **blind/time‑based** (usando `pg_sleep()`).

---

## 5. Evidências

- Reportagem The Hacker News.
- Advisory no GitHub confirmando versões afetadas.
- Registro NVD com métricas e referências.
- Listagens em agencies governamentais (Singapore CSA).

---

## 6. Passos para Reproduzir (em ambiente controlado)

## 6.1 Exemplo real
1. Instale o **Apache Traffic Control 8.0.1** com Traffic Ops.
2. Autentique-se com usuário `admin`.
3. Envie requisição PUT similar:

```http
PUT /api/5.0/deliveryservice_request_comments/123 HTTP/1.1
Host: host
Content-Type: application/json
Authorization:Bearer <token-admin>

{
  "id": "23423'; SELECT pg_sleep(5); --"
}

```

4. Note o atraso de 5 segundos — evidência de injeção SQL time-based.

---

## 6.2 Exemplo simplificado em Python (Flask + SQLite)

1. crie o ambiente virtual ```bash python -m venv venv```
2. instale o Flask ```bash pip install Flask```
3. rode a aplicação ```python app.py```
4. digite 1 --> vai retornar `Estudante Felipe`
4. digite 2 --> vai retornar `Professor Felipe`
5. digite 1 UNION SELECT sqlite_version() --> vai retornar a versão do SQL

**OBS**: O passo 5 exemplifica o conceito do SQLi apresentado contextualizado no problema do apache.

## 7. Sugestões de Mitigação e Correção

- **Atualizar para 8.0.2**.
- Usar **Prepared Statements** ou ORM seguro.
- Validar e filtrar entradas.
- Monitorar usuários privilegiados e logar queries suspeitas.

---

## 8. Referências

- [The Hacker News](https://thehackernews.com/2024/12/critical-sql-injection-vulnerability-in.html)
- [NVD – CVE‑2024‑45387](https://nvd.nist.gov/vuln/detail/cve-2024-45387)
- [GitHub Advisory](https://github.com/advisories/GHSA-vq94-9pfv-ccqr)
- [CYFIRMA Research](https://www.cyfirma.com/research/cve-2024-45387-critical-vulnerability-in-apache-traffic-control/)

---

## 9. Pontuação CVSS

| Métrica                      | Valor           |
|------------------------------|-----------------|
| Vetor Ataque (AV)             | Rede (N)        |
| Complexidade (AC)             | Baixa (L)       |
| Privilégios (PR)              | Baixo (L)       |
| Interação do Usuário (UI)     | Nenhuma (N)     |
| Escopo (S)                    | Inalterado (U)  |
| Confidencialidade (C)         | Alta (H)        |
| Integridade (I)               | Alta (H)        |
| Disponibilidade (A)           | Alta (H)        |
| **Base Score (NVD)**          | **8.8**         |
| **Base Score (Apache)**       | **9.9**         |

---
