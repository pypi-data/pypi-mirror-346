import json
from link_nlp.text_processing.text_generation_unified import TextGenerator
import torch
def load_questions(file_path):
    """Carica le domande dal file JSONL"""
    questions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            questions.append(json.loads(line))
    return questions

def evaluate_answer(generated_answer, correct_answer):
    """Valuta la risposta generata rispetto alla risposta corretta"""
    # Qui potremmo implementare una metrica più sofisticata
    # Per ora facciamo un semplice confronto
    return generated_answer.strip() == correct_answer.strip()

def main():
    # Inizializza il generatore con Qwen3
    generator = TextGenerator(
        model_name="Qwen/Qwen3-8B",  # Usiamo Qwen3
        use_llm=True,  # Usiamo vllm per performance migliori
        device="cuda" if torch.cuda.is_available() else "cpu"
    )
    
    # Carica le domande di test
    questions = load_questions("data/codice_appalti_qa.jsonl")
    
    # Statistiche
    total_questions = len(questions)
    correct_answers = 0
    
    # Testa ogni domanda
    for i, q in enumerate(questions, 1):
        print(f"\nDomanda {i}/{total_questions}:")
        print(f"Q: {q['question']}")
        
        # Genera la risposta
        prompt = f"Rispondi alla seguente domanda sul Codice Appalti italiano: {q['question']}"
        generated_answer = generator.generate_with_llm(prompt)
        
        print(f"Risposta generata: {generated_answer}")
        print(f"Risposta corretta: {q['correct_answer']}")
        
        # Valuta la risposta
        is_correct = evaluate_answer(generated_answer, q['correct_answer'])
        if is_correct:
            correct_answers += 1
        
        print(f"Corretta: {'Sì' if is_correct else 'No'}")
    
    # Stampa le statistiche finali
    accuracy = (correct_answers / total_questions) * 100
    print(f"\nRisultati finali:")
    print(f"Domande totali: {total_questions}")
    print(f"Risposte corrette: {correct_answers}")
    print(f"Accuratezza: {accuracy:.2f}%")

if __name__ == "__main__":
    main()