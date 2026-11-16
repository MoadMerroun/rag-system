def upload( client, pdf_bytes, filename = "sample.pdf" ):
    return client.post( "/documents", files = { "file": ( filename, pdf_bytes, "application/pdf" ) } )


def test_upload_pdf_returns_filename_and_chunk_count( client, sample_pdf ):
    response = upload( client, sample_pdf )

    assert response.status_code == 200
    assert response.json() == { "filename": "sample.pdf", "chunks": 1 }


def test_ask_returns_answer_and_sources( client, sample_pdf ):
    upload( client, sample_pdf )

    response = client.post( "/ask", json = { "question": "What is the capital of Atlantis?" } )

    assert response.status_code == 200
    body = response.json()
    assert body[ "answer" ] == "fake answer"
    assert body[ "sources" ] == [ { "filename": "sample.pdf", "page": 0 } ]


def test_prompt_contains_retrieved_chunk_text( client, sample_pdf, fake_llm ):
    upload( client, sample_pdf )

    client.post( "/ask", json = { "question": "What is the capital of Atlantis?" } )

    prompt = fake_llm.prompts[ -1 ]
    assert "The capital of Atlantis is Poseidonia." in prompt
    assert "What is the capital of Atlantis?" in prompt
    # Only chunk text goes in, not Chroma's raw result dict.
    assert "'ids'" not in prompt
    assert "'metadatas'" not in prompt


def test_ask_requires_a_json_body( client ):
    response = client.post( "/ask", params = { "message": "old style" } )

    assert response.status_code == 422
