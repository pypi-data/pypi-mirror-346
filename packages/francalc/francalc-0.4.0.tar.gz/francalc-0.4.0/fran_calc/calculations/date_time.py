from ..modules import run_test
from datetime import datetime

def calculate_time(horario, horario_a_frente):
    # Converte o horário para minutos
    horas, minutos = map(int, horario.split(':'))
    total_minutos = horas * 60 + minutos

    # Converte o horário a frente para minutos
    horas_a_frente, minutos_a_frente = map(int, horario_a_frente.split(':'))
    total_minutos_a_frente = horas_a_frente * 60 + minutos_a_frente

    # Calcula a diferença em minutos
    diferenca_minutos = total_minutos + total_minutos_a_frente

    # Converte de volta para horas e minutos
    horas_resultado = diferenca_minutos // 60
    minutos_resultado = diferenca_minutos % 60

    return f"{horas_resultado:02}:{minutos_resultado:02}"

def calculate_age(birth_date: str):
    """
    Calcula a idade em anos, meses e dias a partir de duas datas no formato 'YYYY-MM-DD'.
    """

    # Converte as strings para objetos datetime
    birth_date = datetime.strptime(birth_date, '%Y-%m-%d')
    current_date = datetime.now()

    # Calcula a diferença entre as datas
    delta = current_date - birth_date

    # Converte a diferença para anos, meses e dias
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30

    return f"{years} anos, {months} meses, {days} dias"

def calculate_weekday(date: str) -> str:
    """
    Retorna o dia da semana para uma data no formato 'YYYY-MM-DD'.
    """
    date = datetime.strptime(date, '%Y-%m-%d')
    return date.strftime('%A')

def add_business_days(start_date: str, days: int) -> str:
    """
    Adiciona dias úteis a uma data no formato 'YYYY-MM-DD'.
    """
    from numpy import busday_offset

    # Converte a string para um objeto datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()

    # Adiciona os dias úteis
    end_date = busday_offset(start_date, days, roll='forward')

    return end_date

if __name__ == "__main__":
    run_test(calculate_time, '12:30', '02:15')
    run_test(calculate_age, '2010-05-29')
    run_test(calculate_weekday, '2025-05-06')
    run_test(add_business_days, '2025-05-09', 1)