import requests
import matplotlib.pyplot as plt
import csv
from typing import Dict, List
import operator

import os

# Scopus API Key
API_KEY = 'cb3d274f6b959c9b9dfeccf09729d66c'

# List of search terms
search_terms: List[str] = ["Open Data Kit","KoBoToolbox","ona.io","magpi.com","Conseris","Teamscope","SurveyCTO","DHIS2","Logiak","Aam Digital","Enketo Smart Paper","REDCap","betterform.com","Google Forms","LimeSurvey","Formbricks","Nextcloud Forms","GetInput","Typeform","simulai","Tally Forms","SurveyMonkey","Microsoft Forms","Tandem Surveys","Nextcloud Polls","Rapidforms","Chisquares","getsatisfaction.com","Florm","Topgrade Quiz Maker","told.club","Cognito Forms","Crowdsignal","pollly","OhMyForm","UserReport","Yakforms","Tripetto","WoltLab Suite","SurveyLab","Qualtrics","Responster","Paperform","SmartSurvey","Clappia","Drupal Webform","ClassMarker","Getsitecontrol","LiquidFeedback","iSpring QuizMaker","Formstack","Zoho Survey","Getform","SurveyMoz","Kwik Surveys","Webform.com","Survicate","Collect.chat","SoGoSurvey","SurveyPlanet","Journey Surveys","Rational Survey","SurveyNuts","MARE Surveys","Opinionlab","Inqwise","Neurovation.net","Feedback Cat","Zync Free Surveys","PaperSurvey.io","Survio","SurveyGizmo","Refiner.io","Webanketa.com","PollMaker","Engageform","1Flow","eSurv.org","mydatascope.com","Go4Read","CheckMarket","MachForm","Formsort","Spokk","JotForm","EUSurvey","Zoomerang","ChilledLime","Flisti","Facebook Questions","Pollscape","Feedier","BallotBin","CviewSurvey","EventSurvey360","Live Vote","Responsly","123FormBuilder","Enalyzer","Exam.net","ApPHP DataForm","Heedbook","Foresee.com","sentiments.me","Super Simple Survey","boll.co","WonderShare QuizCreator","YesInsights","hellotars","Reactflow","Form2Sheet","Upinion","Nintex Forms","GetFeedback","Eloquant","PriceChecks","PlanSo Forms","youengage","rekommend.io","ngSurvey","Survtapp","LamaPoll","Pollogo","SurveySparrow","Survey Anyplace","Aweform","Formito","Wispform","CusJo","SoSci Survey","eSurveysPro.com","FormCrafts","malvee.com/en/jobber","Wizu","SurveyStatz","CreateSurvey","Sarshomar","SurveyTown","Emojot","Startquestion","interview-efm","Seanote","insta.vote","usario","Sentimy","FormBit","Cisco Webex Experience Management","Callexa Feedback","Pollanimal","ElectionBuddy","QuickTapSurvey","LiveForm","MikeCRM","Free Survey Creator (FSC)","Satsum","polltogo","Retool Forms","ZingPoll","doopoll","survey-ninja","AvidIntelli","Checkbox Survey","Formist.io","CloudRatify","Phonic.ai","AskYourTargetMarket.com","PopSurvey","Wyzerr","Rapidoform","FormsBook","Nexticy Cloud","Obsurvey","Opina: Survey Manager","Insight Stash","iPerceptions","DataWinners","FormNX","E-mail polls by Clubble","pForm","Hubert.ai","SurveyLegend","SurveyMethods","VerticalResponse Online Survey","Examinare Survey Tool","Mobenzi Researcher","Liveworksheets","PandaForm","Pulse Insights","Nicereply","FormDesigner","merren.io","OpenPoll","VaultForm","Sissurvey","Keenforms","AskNicely","Feedback Button","erhebung.de","Swurveys","ApPHP Survey","Quilgo","FormSite","MoboSurvey","Findmind","surveyproject.com","Zapof Forms","JoInTest","QuestionScout","DocsCloud","looping.com","Form 'n Go","MicroPoll","HOTforms123","Captisa Forms","Device Magic","Sales Essistant","WinSurvey","Yought","Amazon Mechanical Turk","participaid","buildarray","responses.me","pnguin.app/agree","Fillout","SurveyJS","MakeForms","Weavely","Yay! Forms","Formsnow","BEEKAI","Nerdy Form","LiberaForms","VFront","Wufoo","Quill Forms","formtools.org","Handypolls","PollUnit","alpina.io","FeedbackSpark","Formester","Form2chat","Pabbly Form Builder","Fabform","neetoForm","biznessmaker","MightyForms","Riley Form Maker","Faary","SurveyNova","Contlo","Whirr","Rational ClearQuest","FormBucket","Superdocu","d21.me","Formitty","Formbox","MangoCRM","Wolf Responsive Form Maker","PHP FormBuilder","Forms.app","freifeld.emphasize.de","Touch Forms Pro","FormKeep","ENKETO ONE","Vanjaro","Formjelly","Sheet Monkey","Fastboss","Inspakt","JotJab","weForms","ClaySys AppForms","BlockSurvey","Peasy Forms","Awesome Forms","Regpack","getformly.com","CompanyHub CRM","FormToEmail","FormPress","Vue Flow Form","Carrrot","ManyContacts","KPI.Com","Jigloo","multiform.com","See Memo","marketablellc.com","Collector AI","K2 blackperl","Zoho Forms","QuestionPro","Youform","Survs","Easydus","iFormBuilder","Akin Persona Tool","FormForAll","AbcSubmit","devolute.cloud","CourseStorm","Fieldboom","getsimpleform.com","Orbitrics","Sysflows","Malcolm.app","Firesales.io","Zurvey.io","Zapflow","Screendoor","Porsline","Eval&GO","Forma (getforma.co)","FORMCLICK","Startup Manager","IBM Forms Experience Builder","EngageVisitor"]

yearRange = range(1990, 2023)

def get_publication_count(term: str, year: int = None) -> int:
    """
    Function to retrieve the number of publications for a given term in a specific year.

    Args:
        term (str): The search term.
        year (int): The publication year.

    Returns:
        int: The number of publications.
    """
    url: str = 'https://api.elsevier.com/content/search/scopus'
    headers: Dict[str, str] = {'X-ELS-APIKey': API_KEY}
    params: Dict[str, Union[str, int]] = {
        'count': '1'  # We only need to check if there are any results
    }

    if year is None:
        params['query'] = f'ALL("{term}")'
    else:
        params['query'] = f'ALL("{term}") AND PUBYEAR = {year}'

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # Raise an exception for non-200 status codes
        data: Dict[str, str] = response.json()
        total_results: int = int(data['search-results']['opensearch:totalResults'])
        print(f"Number of results for '{term}' in {year}: {total_results}")
        return total_results
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving data for '{term}' in {year}: {e}")
        return None

def load_cached_data() -> Dict[str, Dict[int, int]]:
    """
    Function to load cached data from CSV file.

    Returns:
        Dict[str, Dict[int, int]]: Dictionary containing cached publication counts.
    """
    publication_counts: Dict[str, Dict[(str|int), int]] = {}
    try:
        with open('publication_counts.csv', 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                term = row['Term']
                publication_counts[term] = {}
                publication_counts[term]['Total'] = int(row['Total'])
                for column, count in row.items():
                    if column != 'Term' and column != 'Total' and count is not '' and count is not None:
                        year = int(column)
                        publication_counts[term][year] = int(count) 
    except FileNotFoundError:
        pass
    return publication_counts

def save_cache(publication_counts: Dict[str, Dict[int, int]]) -> None:
    """
    Function to save the publication counts cache to a CSV file.

    Args:
        publication_counts (Dict[str, Dict[int, int]]): Dictionary containing publication counts.
    """
    sortedItems = sorted(publication_counts.items(), key=lambda item: item[1]["Total"], reverse= True)
    
    with open('publication_counts.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Term'] + ["Total"] + [*yearRange])  # Write header
        for item in sortedItems:
            term = item[0]
            row = [term] + [publication_counts[term]["Total"]] + [publication_counts[term][year] for year in yearRange if year in publication_counts[term]]
            writer.writerow(row)

def main() -> None:
    """
    Main function to fetch publication counts for each term and plot the trend.
    """
    # Load cached data
    publication_counts: Dict[str, Dict[int, int]] = load_cached_data()

    for term in search_terms:
        if term not in publication_counts or "Total" not in publication_counts[term]:
            total_publication_count = get_publication_count(term)
            publication_counts[term] = {"Total": total_publication_count}
            save_cache(publication_counts)

    for term in search_terms:
        for year in yearRange:
            if year not in publication_counts[term] or publication_counts[term][year] is None:
                if publication_counts[term]["Total"] > 35000 or publication_counts[term]["Total"] == 0:
                    publication_counts[term][year] = None
                    continue
                
                publication_counts[term][year] = get_publication_count(term, year)
                save_cache(publication_counts)

    plot_data = {}
    for term, counts in sorted(publication_counts.items(), key=lambda item: item[1]["Total"], reverse= True):
        if publication_counts[term]["Total"] > 35000 or publication_counts[term]["Total"] < 195:
            continue    
        for year in publication_counts[term]:
            if year == "Total":
                continue
            if term not in plot_data:
                plot_data[term] = {}                     
            plot_data[term][year] = publication_counts[term][year]

    # Create trend plot

 

    plt.figure(figsize=(10, 6))
    for term, counts in plot_data.items():
        years = list(counts.keys())
        counts = list(counts.values())
        plt.plot(years, counts, label=term)

    plt.title('Number of Publications per Year')
    plt.xlabel('Year')
    plt.ylabel('Number of Publications')
    plt.legend(title='Search Terms')
    plt.grid(True)
    
    # Save the plot as a PDF file
    plt.savefig("publication_trend.pdf", bbox_inches="tight")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()