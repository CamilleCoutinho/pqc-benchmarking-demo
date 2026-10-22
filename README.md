# pqc-benchmarking-demo

Script em Python para medição, avaliação e comparação de desempenho entre a criptografia assimétrica clássica (**RSA-3072**) e o mecanismo de encapsulamento de chaves pós-quântico **ML-KEM** (Module-Lattice-Based Key-Encapsulation Mechanism, antigo Kyber), padronizado pelo NIST (FIPS 203).

O projeto é executado de forma totalmente containerizada via **Docker**, garantindo a compilação nativa da biblioteca C `liboqs` (Open Quantum Safe) e a reprodutibilidade dos testes de segurança em qualquer ambiente.

---

## Por que este projeto existe?

A segurança dos algoritmos de chave pública clássicos (como RSA e ECC) fundamenta-se na dificuldade computacional da fatoração de inteiros e do logaritmo discreto. Com o avanço da computação quântica, o **Algoritmo de Shor** tornará esses esquemas vulneráveis a ataques em tempo polinomial.

Embora computadores quânticos de grande escala ainda estejam em desenvolvimento, o ecossistema de cibersegurança enfrenta a ameaça de ataques do tipo *"Harvest Now, Decrypt Later"* (interceptar e armazenar tráfego cifrado hoje para decifrá-lo no futuro). Em resposta, o NIST padronizou os primeiros algoritmos de Criptografia Pós-Quântica (PQC).

Diante do processo de transição tecnológica, surge a questão prática: **qual é o impacto de desempenho e o custo de processamento ao migrar para a PQC?** Este projeto busca responder a essa pergunta através de testes práticos de latência e benchmarking de código.

---

## Objetivos

- **Benchmarking de Latência:** Medir o tempo de execução (em milissegundos) para **Geração de Chaves**, **Encapsulamento/Cifragem** e **Decapsulamento/Decifragem** entre o RSA-3072 e o ML-KEM (níveis de segurança 512, 768 e 1024).
- **Integração Prática com PQC:** Utilizar as ferramentas da *Open Quantum Safe* (`liboqs` e `liboqs-python`) para demonstrar como chamadas de KEM (*Key Encapsulation Mechanism*) funcionam no nível de código.
- **Ambiente Reprodutível via Docker:** Disponibilizar um `Dockerfile` multi-stage/autônomo que realiza a compilação nativa em C da `liboqs`, dispensando a instalação e compilação manual de dependências no sistema hospedeiro.
- **Base para Pesquisa Acadêmica:** Servir como protótipo de estudo para projetos de P&D em cibersegurança e preparação para pós-graduação/mestrado na área.

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.10+
- **Criptografia Pós-Quântica:** `liboqs` (Open Quantum Safe C Library) & `liboqs-python`
- **Criptografia Clássica:** `cryptography` (OpenSSL backend)
- **Formatador de Resultados:** `tabulate`
- **Containerização:** Docker (Debian `python:3.10-slim` com compilação `cmake` / `gcc`)

---

## O que o script mede

O script executa o ciclo completo de troca/estabelecimentos de segredo para cada algoritmo e gera uma tabela explicativa no terminal:

| Operação no Benchmark | RSA-3072 (OAEP) | ML-KEM (PQC / Kyber) |
| :--- | :--- | :--- |
| **Geração de Chaves** | `generate_private_key` | `generate_keypair` |
| **Encapsulamento/Cifragem** | `public_key.encrypt` | `encap_secret` |
| **Decapsulamento/Decifragem** | `private_key.decrypt` | `decap_secret` |

---

## Como Executar

### Pré-requisitos
- **Docker Engine / Docker Desktop** instalado e em execução.

### Passo a Passo

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/CamilleCoutinho/pqc-benchmarking-demo.git
   cd pqc-benchmarking-demo
   ```

2. **Construa a imagem Docker (compilação da `liboqs` e instalação de dependências):**
   ```bash
   docker build -t pqc-benchmark .
   ```

3. **Execute o benchmark no container:**
   ```bash
   docker run --rm pqc-benchmark
   ```

---

## Exemplo de Saída Esperada

```text
+---------------------+-----------------+------------------+------------------+
| Algoritmo           | keygen (ms)     | encap/enc (ms)   | decap/dec (ms)   |
+=====================+=================+==================+==================+
| RSA-3072 (OAEP)     | 168.855         | 0.051            | 2.069            |
+---------------------+-----------------+------------------+------------------+
| ML-KEM-512          | 0.015           | 0.017            | 0.018            |
+---------------------+-----------------+------------------+------------------+
| ML-KEM-768          | 0.019           | 0.019            | 0.020            |
+---------------------+-----------------+------------------+------------------+
| ML-KEM-1024         | 0.020           | 0.022            | 0.025            |
+---------------------+-----------------+------------------+------------------+
```

---

## Interpretação dos Resultados e Limitações

- **Velocidade de Processamento:** O ML-KEM demonstra ser significativamente mais rápido que o RSA-3072 na geração de chaves e na operação de decapsulamento/decifragem.
- **Tamanho dos Artefatos (Overhead de Rede):** Embora mais rápido computacionalmente, os algoritmos pós-quânticos possuem chaves públicas e textos cifrados de tamanho superior aos das curvas elípticas (ECC), o que impacta o consumo de largura de banda e protocolos de rede.
- **Camada de Abstração:** A medição inclui o *overhead* natural dos bindings Python para as bibliotecas C nativas.

---

## Estrutura do Repositório

```text
.
├── Dockerfile         # Configuração do ambiente Linux, compilação da liboqs e setup
├── requirements.txt   # Dependências Python (liboqs-python, cryptography, tabulate)
├── benchmark.py       # Script principal em Python para medições e exibição da tabela
└── README.md          # Documentação do projeto
```

---

## Próximos Passos e Melhorias Futuras

- [ ] Incluir medições de tamanho (bytes) da chave pública, chave privada e ciphertext.
- [ ] Adicionar algoritmos de Assinatura Digital Pós-Quântica (ML-DSA / Dilithium e SLH-DSA / SPHINCS+).
- [ ] Exportação automática dos resultados para arquivos CSV/JSON para análise estatística.
- [ ] Implementar suporte a testes com algoritmos híbridos (Clássico + PQC).

---

## Referências

- **NIST FIPS 203:** [Module-Lattice-Based Key-Encapsulation Mechanism Standard](https://csrc.nist.gov/pubs/fips/203/final)
- **Open Quantum Safe Project:** [openquantumsafe.org](https://openquantumsafe.org/)
- **PQ-Crystals:** [pq-crystals.org](https://pq-crystals.org/)

---

## Licença

Este projeto é disponibilizado sob a licença [MIT](LICENSE).