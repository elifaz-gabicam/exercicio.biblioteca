<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Biblioteca SENAI</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        h1 {
            text-align: center;
            color: #333;
        }
        label {
            display: block;
            margin-bottom: 8px;
            font-weight: bold;
        }
        input[type="text"], input[type="number"], textarea {
            width: 100%;
            padding: 10px;
            margin-bottom: 12px;
            border: 1px solid #ccc;
            border-radius: 4px;
        }
        textarea {
            height: 100px;
            resize: vertical;
        }
        button {
            display: block;
            width: 100%;
            padding: 10px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }
        th {
            background-color: #007bff;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        .no-books {
            text-align: center;
            color: #777;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sistema de Biblioteca SENAI</h1>
        <form id="bookForm">
            <label for="titulo">Título do Livro</label>
            <input type="text" id="titulo" name="titulo" required>

            <label for="autor">Autor</label>
            <input type="text" id="autor" name="autor" required>

            <label for="ano">Ano de Publicação</label>
            <input type="number" id="ano" name="ano" min="1000" max="9999" required>

            <label for="descricao">Descrição</label>
            <textarea id="descricao" name="descricao" required></textarea>

            <button type="submit">Adicionar Livro</button>
        </form>

        <table id="bookTable">
            <thead>
                <tr>
                    <th>Título</th>
                    <th>Autor</th>
                    <th>Ano</th>
                    <th>Descrição</th>
                </tr>
            </thead>
            <tbody>
                <tr class="no-books">
                    <td colspan="4">Nenhum livro cadastrado.</td>
                </tr>
            </tbody>
        </table>
    </div>

    <script>
        document.getElementById('bookForm').addEventListener('submit', function(event) {
            event.preventDefault();

            // Get form values
            const titulo = document.getElementById('titulo').value;
            const autor = document.getElementById('autor').value;
            const ano = document.getElementById('ano').value;
            const descricao = document.getElementById('descricao').value;

            // Create new table row
            const tableBody = document.getElementById('bookTable').querySelector('tbody');
            const newRow = tableBody.insertRow();
            newRow.insertCell(0).textContent = titulo;
            newRow.insertCell(1).textContent = autor;
            newRow.insertCell(2).textContent = ano;
            newRow.insertCell(3).textContent = descricao;

            // Remove "No books" message if it exists
            if (tableBody.querySelector('.no-books')) {
                tableBody.querySelector('.no-books').remove();
            }

            // Reset form
            document.getElementById('bookForm').reset();
        });
    </script>
</body>
</html>
