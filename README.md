README: Assistente de Suporte Técnico de TI
Descrição
Este projeto visa automatizar o suporte técnico de TI, oferecendo diagnóstico e soluções para problemas comuns de internet, software e hardware. O assistente usa IA para entender a descrição do problema e sugerir soluções de forma rápida. Se o problema persistir, ele pode registrar um chamado de suporte.

Funcionalidades
Diagnóstico de Problemas: A IA analisa o problema descrito e sugere soluções com base em uma base de conhecimento.
Registro de Chamados: Se o problema não for resolvido, o usuário pode registrar um chamado com descrição e prioridade.
Histórico de Conversa: Mantém um histórico de interações, ajudando a fornecer respostas mais precisas e contextuais.
Casos de Uso
Exemplo 1: Problema de Internet
Entrada: "Minha internet está lenta e cai constantemente."
Saída:

diff
Copiar código
Categoria: internet
Sintoma: conexão lenta

Soluções:
- Reinicie o roteador
- Verifique os cabos de rede
- Teste com outro dispositivo
Exemplo 2: Problema de Software
Entrada: "O programa não está abrindo."
Saída:

diff
Copiar código
Categoria: software
Sintoma: erro ao iniciar

Soluções:
- Reinicie o computador
- Verifique atualizações
- Execute verificação de arquivos do sistema
Exemplo 3: Problema de Hardware
Entrada: "O computador não liga."
Saída:

diff
Copiar código
Categoria: hardware
Sintoma: não liga

Soluções:
- Verifique a conexão de energia
- Teste a fonte de alimentação
- Verifique as conexões internas
Exemplo 4: Registro de Chamado
Entrada: Dados JSON com problema:

json
Copiar código
{
    "descricao": "Computador não liga",
    "prioridade": "alta"
}
Saída: "Chamado 20241205123045 registrado com sucesso!"

Como Executar
Requisitos
Python 3.x
Bibliotecas: streamlit, langchain, huggingface_hub, json
Token Hugging Face: Para usar o modelo de IA, você precisa de um token de acesso.
Passos
Clone o repositório ou baixe o código.
Instale as dependências:
bash
Copiar código
pip install -r requirements.txt
Configure o Token Hugging Face: Obtenha o token no Hugging Face e insira-o no campo de configuração do Streamlit.
Execute a aplicação:
bash
Copiar código
streamlit run app.py
Acesse o app em http://localhost:8501 e interaja com o assistente.
Vantagens da Abordagem com IA
Eficiência: O assistente responde rapidamente, sem a necessidade de intervenção humana.
Precisão: A IA analisa as descrições dos problemas com base em uma base de conhecimento e oferece soluções adequadas.
Escalabilidade: Pode atender muitos usuários ao mesmo tempo, sem sobrecarregar a equipe de suporte.
Disponibilidade 24/7: Oferece suporte a qualquer hora, sem precisar esperar por atendimento
