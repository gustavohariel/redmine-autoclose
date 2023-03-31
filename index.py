from redminelib import Redmine,exceptions
from datetime import datetime
from dateutil import parser
import json


# dict para gerar um log JSON
issue_map = {}
# url do Redmine
redmine_url = "baseurl do redmine"
# api key do redmine
redmine_key = "sua API key"

def main():

    today = datetime.today().isoformat()
    date1 = parser.parse(today)

    redmine = Redmine(redmine_url, key=redmine_key)

    # define parametro de busca dos chamados
    issues = redmine.issue.filter(
        status_id="3",
        created_on=">=2017-01-01",
        sort="updated_on",
        include="journals"
    )

    #para cada chamado selecionado, compara a data atual com o ultimo update do chamado.
    # se diff >= 7, atualiza o status para fechado com a data de fechamento e adiciona uma nota (journal) no chamado.
    # se sucesso no update, armazena dados e url do chamado para logs.

    for issue in issues:
        date2 = parser.parse(issue.updated_on.isoformat())
        diff = date1 - date2
        if diff.days >= 7:
            try:
                redmine.issue.update(
                    1,
                    notes="Fechado Pela Rotina Automatica Pois Estava No Status Resolvido a Mais de 7 dias",
                    closed_on=date1,
                    status_id=5)
            except exceptions.ValidationError(BaseException) :
                return "error"
            else:
                issue_map[issue.id] = (issue.subject,redmine_url + "/issues/" + str(issue.id))
                print(str(issue.id) + " - Chamado Atualizado")

    # se existe algum chamado atualizado, criar log.
    if issue_map:
        with open(f"logs/closed-logs-{datetime.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as json_out:
            json.dump(issue_map, json_out)            


    
if __name__ == "__main__":
    main()
    exit("Fim do Script")
