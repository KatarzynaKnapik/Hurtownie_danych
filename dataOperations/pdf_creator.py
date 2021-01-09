from IPython.display import display, HTML
from xhtml2pdf import pisa  

graphs = [
    'Screen_plot.png',
    'CPU_plot.png',
    'Memory_plot.png',
    'Storage_plot.png'
]

def repot_template(graph_url):
    return f'<div> <img style="height: 500px;" src="{graph_url}"> </div>'   
 

report_html = ''
head = '<head><meta http-equiv="content-type" content="text/html; charset=utf-8"></head>' 
header = '<h1>Hurtownie Danych 2020/2021</h1><br><hr>'
authors = '''<h3>Knapik Katarzyna</h3>
          <h3>Kwolek Krzysztof</h3>
          <h3>Lippa Andrzej</h3><hr>''' 
opis = '''<p>Dane, wykorzystane do rysowania poniższych wykresów, zostały pobrane z portalu 
<a href="https://www.ceneo.pl/Laptopy" >CENEO.</a></p>
        <p>Na podstawie danych stworzonu cztery wykresy: </p> 
        <ul>
            <li> 1. Średnia cena względem rozmiaru ekranu.</li>
            <li> 2. Średnia cena względem mocy procesora.</li>
            <li> 3. Średnia cena względem pamięci operacyjnej RAM.</li>
            <li> 1. Średnia cena względem pojemności dysku.</li>
        </ul>'''     
t = ["<h2>1. Średnia cena względem rozmiaru ekranu.</h2>",
 "<h2>2. Średnia cena względem mocy procesora.</h2>",
 "<h2>3. Średnia cena względem pamięci operacyjnej RAM.</h2>",
 "<h2>1. Średnia cena względem pojemności dysku.</h2>"]

content = head + header + authors + opis 

for count, graph_url in enumerate(graphs):
    content += f'{t[count]}' 
    content += repot_template('C:\\Users\\Katarzyna Knapik\\Documents\\PY\\Scraping\\HD_scrapy\\priceComparison\\' + graph_url)


def convert_html_to_pdf(source_html, output_filename):
    result_file = open(output_filename, "w+b")

    pisa_status = pisa.CreatePDF(
        source_html.encode('utf-8'),
        dest=result_file,
        encoding='utf-8'    
    )

    result_file.close()
    return pisa_status.err


convert_html_to_pdf(content, 'report.pdf')
