from app.vector_store import query_similar
import ollama

def retrieve_and_answer(question: str) -> tuple[str, list[str]]:
    question_context = query_similar(question)

    if not question_context['documents'][0]:
        return ("Das kann ich anhand des Kontextes nicht beantworten.", [])

    joined_sources = "\n".join(question_context['documents'][0])

    system_Prompt = (
      "Du bist ein Lernhelfer. "
      "Beantworte die Frage des Nutzers ausschließlich auf Basis des bereitgestellten Kontextes. "
      "Wenn der Kontext die Antwort nicht hergibt, antworte mit 'Das kann ich anhand des Kontextes nicht beantworten.'\n\n"
      f"KONTEXT:\n{joined_sources}" #ich schätze eig muss ich eine liste aus allen contents zurückgeben?
    ) 

    response = ollama.chat(
        model="qwen2.5:7b",
        messages = [
          {"role": "system", "content":system_Prompt},
          {"role": "user", "content": question}
        ]
    )

    metadata = []

    for value in question_context['metadatas'][0]:
        source = value['source']
        page = value['page']

        s = source + " " + str(page)
        
        
        metadata.append(s)
        

    return (response['message']['content'], metadata)

