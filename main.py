import requests
from datetime import datetime
import csv
from typing import List, Dict, Tuple
import pandas as pd
from scipy import stats

def get_top_repos_data(orgs: List[str] = ["facebook", "microsoft", "google"]) -> List[Dict]:
    """
    Coleta os 10 repositórios mais populares (por estrelas) de cada organização
    e retorna suas informações detalhadas
    """
    print("Iniciando coleta de dados dos repositórios...")
    github_token = "SUA_CHAVE_AQUI"
    
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    all_repos = []
    
    for org in orgs:
        print(f"\nColetando dados da organização: {org}")
        try:
            # Obtém os repositórios ordenados por estrelas (descendente)
            response = requests.get(
                f"https://api.github.com/orgs/{org}/repos",
                headers=headers,
                params={
                    "sort": "stars",
                    "direction": "desc",
                    "per_page": 100,
                    "type": "public"
                }
            )
            response.raise_for_status()
            
            repos = response.json()
            print(f"- Encontrados {len(repos)} repositórios")
            
            # Pega os 10 repositórios com mais estrelas
            top_10_repos = sorted(repos, key=lambda x: x['stargazers_count'], reverse=True)[:10]
            
            for repo in top_10_repos:
                print(f"  - Processando repositório: {repo['name']} ({repo['stargazers_count']} estrelas)")
                
                # Obtém informações detalhadas do repositório
                repo_detail = requests.get(
                    f"https://api.github.com/repos/{org}/{repo['name']}",
                    headers=headers
                ).json()
                
                # Obtém número total de pull requests aceitas
                pulls_url = f"https://api.github.com/repos/{org}/{repo['name']}/pulls"
                pulls = requests.get(
                    pulls_url,
                    headers=headers,
                    params={"state": "closed", "per_page": 1}
                )
                
                # Extrai o total de PRs do header Link ou usa 0 se não houver
                total_pulls = 0
                if 'Link' in pulls.headers:
                    try:
                        total_pulls = int(pulls.headers['Link'].split('page=')[-1].split('>')[0])
                    except (IndexError, ValueError):
                        total_pulls = 0
                
                # Obtém número total de releases
                releases_url = f"https://api.github.com/repos/{org}/{repo['name']}/releases"
                releases = requests.get(
                    releases_url,
                    headers=headers,
                    params={"per_page": 1}
                )
                
                # Extrai o total de releases do header Link ou usa 0 se não houver
                total_releases = 0
                if 'Link' in releases.headers:
                    try:
                        total_releases = int(releases.headers['Link'].split('page=')[-1].split('>')[0])
                    except (IndexError, ValueError):
                        total_releases = 0
                
                # Cria dicionário com informações do repositório
                repo_info = {
                    "organização": org,
                    "nome": repo['name'],
                    "estrelas": repo['stargazers_count'],
                    "data_criação": repo['created_at'],
                    "última_atualização": repo['updated_at'],
                    "total_issues": repo_detail['open_issues_count'],
                    "pull_requests_aceitas": total_pulls,
                    "total_releases": total_releases,
                    "linguagem": repo.get('language', 'Não especificada'),
                    "descrição": repo.get('description', 'Sem descrição'),
                    "forks": repo['forks_count']
                }
                
                all_repos.append(repo_info)
                
        except requests.exceptions.RequestException as e:
            print(f"Erro ao obter dados da organização {org}: {str(e)}")
            continue
    
    # Salva os dados em CSV
    with open('repositorios_top10.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            "organização", "nome", "estrelas", "data_criação", "última_atualização",
            "total_issues", "pull_requests_aceitas", "total_releases",
            "linguagem", "descrição", "forks"
        ])
        writer.writeheader()
        writer.writerows(all_repos)
    
    print(f"\nTotal de repositórios processados: {len(all_repos)}")
    print("Dados salvos em 'repositorios_top10.csv'")
    return all_repos

def realizar_testes_anova(dados_csv: str = 'repositorios_top10.csv') -> Dict[str, Tuple[float, float, str]]:
    """
    Realiza testes ANOVA para cada métrica entre as organizações
    
    Returns:
        Dict com resultados dos testes (estatística F, p-valor e interpretação)
    """
    print("\nRealizando testes ANOVA...")
    
    # Lê o CSV com os dados
    df = pd.read_csv(dados_csv)
    
    # Converte datas para calcular idade e tempo desde última atualização
    # Força todas as datas para UTC
    df['data_criação'] = pd.to_datetime(df['data_criação']).dt.tz_localize(None)
    df['última_atualização'] = pd.to_datetime(df['última_atualização']).dt.tz_localize(None)
    hoje = pd.Timestamp.now().tz_localize(None)
    
    # Calcula idade em dias
    df['idade_dias'] = (hoje - df['data_criação']).dt.days
    df['dias_ultima_atualizacao'] = (hoje - df['última_atualização']).dt.days
    
    # Métricas a serem analisadas
    metricas = {
        'idade_dias': 'Idade do Repositório (dias)',
        'total_issues': 'Total de Issues',
        'pull_requests_aceitas': 'Pull Requests Aceitas',
        'total_releases': 'Total de Releases',
        'dias_ultima_atualizacao': 'Dias desde Última Atualização'
    }
    
    resultados = {}
    
    # Realiza ANOVA para cada métrica
    for coluna, nome in metricas.items():
        # Separa dados por organização
        grupos = [
            df[df['organização'] == org][coluna].values
            for org in ['facebook', 'microsoft', 'google']
        ]
        
        # Realiza o teste ANOVA
        f_stat, p_valor = stats.f_oneway(*grupos)
        
        # Interpreta o resultado
        interpretacao = (
            "Há diferença significativa entre as organizações"
            if p_valor < 0.05
            else "Não há diferença significativa entre as organizações"
        )
        
        resultados[nome] = (f_stat, p_valor, interpretacao)
        
        print(f"\nANOVA - {nome}")
        print(f"Estatística F: {f_stat:.4f}")
        print(f"P-valor: {p_valor:.4f}")
        print(f"Interpretação: {interpretacao}")
    
    # Salva resultados em CSV
    with open('resultados_anova.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Métrica', 'Estatística F', 'P-valor', 'Interpretação'])
        for metrica, (f_stat, p_valor, interp) in resultados.items():
            writer.writerow([metrica, f_stat, p_valor, interp])
    
    print("\nResultados salvos em 'resultados_anova.csv'")
    return resultados

if __name__ == "__main__":
    # Primeiro coleta os dados
    get_top_repos_data()
    
    # Depois realiza os testes ANOVA
    realizar_testes_anova()
