import json
import os
from operator import itemgetter

import tempfile
from subprocess import run

dir_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../examples'))


def test_inverted_index() -> None:
    input_data = '{"doc_id": 1, "text": "word1 word2"}\n{"doc_id": 2, "text": "word1 word3"}'
    answer = [{'doc_id': 1, 'text': 'word1', 'tf_idf': 0.0},
              {'doc_id': 1, 'text': 'word2', 'tf_idf': 0.34657359027997264},
              {'doc_id': 2, 'text': 'word1', 'tf_idf': 0.0},
              {'doc_id': 2, 'text': 'word3', 'tf_idf': 0.34657359027997264}]

    script_path = dir_path + '/run_inverted_index.py'
    with (tempfile.NamedTemporaryFile("w+", delete=False) as input_file,
          tempfile.NamedTemporaryFile("w+", delete=False) as output_file):
        input_file.write(input_data)
        input_file.close()

        run(["python", script_path, "--input", input_file.name, "--output",
             output_file.name], check=True)
        output = output_file.read()
        output = output.replace("'", '"')
    lines = output.strip().split("\n")
    parsed_output = [json.loads(line) for line in lines]
    assert sorted(parsed_output, key=itemgetter('doc_id', 'text')) == answer


def test_word_count() -> None:
    input_data = '{"doc_id": 1, "text": "word1 word2"}\n{"doc_id": 2, "text": "word1 word3"}'
    answer = [{'count': 1, 'text': 'word2'},
              {'count': 1, 'text': 'word3'},
              {'count': 2, 'text': 'word1'}]
    script_path = dir_path + '/run_word_count.py'

    with (tempfile.NamedTemporaryFile("w+", delete=False) as input_file,
          tempfile.NamedTemporaryFile("r", delete=False) as output_file):
        input_file.write(input_data)
        input_file.close()

        run(["python", script_path, "--input", input_file.name, "--output",
             output_file.name], check=True)
        output = output_file.read()
        output = output.replace("'", '"')
    lines = output.strip().split("\n")
    parsed_output = [json.loads(line) for line in lines]
    assert parsed_output == answer


def test_pmi() -> None:
    input_data = ('{"doc_id": 1, "text": "hello, little world"}'
                  '\n{"doc_id": 2, "text": "little"}'
                  '\n{"doc_id": 3, "text": "little little little"}'
                  '\n{"doc_id": 4, "text": "little? hello little world"}'
                  '\n{"doc_id": 5, "text": "HELLO HELLO! WORLD..."}'
                  '\n{"doc_id": 6, "text": "world? world... world!!! WORLD!!! HELLO!!! HELLO!!!!!!!"}')

    answer = [{'text': 'little', 'doc_id': 3, 'pmi': 0.9555114450274362},
              {'text': 'little', 'doc_id': 4, 'pmi': 0.9555114450274362},
              {'text': 'hello', 'doc_id': 5, 'pmi': 1.1786549963416462},
              {'text': 'hello', 'doc_id': 6, 'pmi': 0.08004270767353636},
              {'text': 'world', 'doc_id': 6, 'pmi': 0.7731898882334817}]
    script_path = dir_path + '/run_pmi.py'

    with (tempfile.NamedTemporaryFile("w+", delete=False) as input_file,
          tempfile.NamedTemporaryFile("r", delete=False) as output_file):
        input_file.write(input_data)
        input_file.close()

        run(["python", script_path, "--input", input_file.name, "--output",
             output_file.name],
            check=True)
        output = output_file.read()
        output = output.replace("'", '"')
    lines = output.strip().split("\n")
    parsed_output = [json.loads(line) for line in lines]
    assert sorted(parsed_output, key=itemgetter('doc_id', 'text')) == answer


def test_yandex_maps() -> None:
    input_length_data = \
        ('{"start": [37.84870228730142, 55.73853974696249], "end": [37.8490418381989, 55.73832445777953],'
         '"edge_id": 8414926848168493057}\n{"start": [37.524768467992544, 55.88785375468433], "end": '
         '[37.52415172755718, 55.88807155843824],"edge_id": 5342768494149337085}\n{"start": '
         '[37.56963176652789, 55.846845586784184], "end": [37.57018438540399, 55.8469259692356],"edge_id": '
         '5123042926973124604}\n{"start": [37.41463478654623, 55.654487907886505], "end": [37.41442892700434, '
         '55.654839486815035],"edge_id": 5726148664276615162}\n{"start": [37.584684155881405, 55.78285809606314], '
         '"end": [37.58415022864938, 55.78177368734032],"edge_id": 451916977441439743}\n{"start": [37.736429711803794, '
         '55.62696328852326], "end": [37.736344216391444, 55.626937723718584],"edge_id": 7639557040160407543}\n'
         '{"start": [37.83196756616235, 55.76662947423756], "end": [37.83191015012562, 55.766647034324706],"edge_id":'
         ' 1293255682152955894}')

    input_time_data = \
        (
            '{"leave_time": "20171020T112238.723000", "enter_time": "20171020T112237.427000","edge_id": '
            '8414926848168493057}''\n{"leave_time": "20171011T145553.040000", "enter_time": "20171011T145551.957000",'
            '"edge_id": ''8414926848168493057}\n{"leave_time": "20171020T090548.939000", "enter_time": '
            '"20171020T090547.463000"'',"edge_id": 8414926848168493057}\n{"leave_time": "20171024T144101.879000",'
            ' "enter_time": ''"20171024T144059.102000","edge_id": 8414926848168493057}\n'
            '{"leave_time": "20171022T131828.330000"'', "enter_time": "20171022T131820.842000","edge_id": '
            '5342768494149337085}\n{"leave_time": ''"20171014T134826.836000", "enter_time": "20171014T134825.215000",'
            '"edge_id": 5342768494149337085}\n'
            '{"leave_time": "20171010T060609.897000", "enter_time": "20171010T060608.344000","edge_id": '
            '5342768494149337085}\n{"leave_time": "20171027T082600.201000", "enter_time": "20171027T082557.571000"'
            ',"edge_id": 5342768494149337085}')

    answer = [{'weekday': 'Fri', 'hour': 8, 'speed': 62.23226147737125},
              {'weekday': 'Fri', 'hour': 9, 'speed': 78.10704542963656},
              {'weekday': 'Fri', 'hour': 11, 'speed': 88.95524618375273},
              {'weekday': 'Sat', 'hour': 13, 'speed': 100.96906087938703},
              {'weekday': 'Sun', 'hour': 13, 'speed': 21.85775209474978},
              {'weekday': 'Tue', 'hour': 6, 'speed': 105.39011441435053},
              {'weekday': 'Tue', 'hour': 14, 'speed': 41.5145837429397},
              {'weekday': 'Wed', 'hour': 14, 'speed': 106.45059931130521}]
    script_path = dir_path + '/run_yandex_maps.py'
    with tempfile.NamedTemporaryFile("w+", delete=False) as time_file, \
            tempfile.NamedTemporaryFile("w+", delete=False) as length_file, \
            tempfile.NamedTemporaryFile("r", delete=False) as output_file:
        time_file.write(input_time_data)
        time_file.close()

        length_file.write(input_length_data)
        length_file.close()

        run(["python", script_path, "--input_time", time_file.name,
             "--input_length",
             length_file.name, "--output", output_file.name], check=True)
        output = output_file.read()
        output = output.replace("'", '"')
    lines = output.strip().split("\n")
    parsed_output = [json.loads(line) for line in lines]
    assert sorted(parsed_output, key=itemgetter('weekday', 'hour')) == answer
