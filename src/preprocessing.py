import re


# Palabras reservadas principales de C++.
# Si encontramos una de estas, la conservamos como palabra clave.
KEYWORDS = {
    "alignas", "alignof", "and", "and_eq", "asm", "auto",
    "bitand", "bitor", "bool", "break", "case", "catch",
    "char", "char16_t", "char32_t", "class", "compl", "const",
    "constexpr", "const_cast", "continue", "decltype", "default",
    "delete", "do", "double", "dynamic_cast", "else", "enum",
    "explicit", "export", "extern", "false", "float", "for",
    "friend", "goto", "if", "inline", "int", "long", "mutable",
    "namespace", "new", "noexcept", "not", "not_eq", "nullptr",
    "operator", "or", "or_eq", "private", "protected", "public",
    "register", "reinterpret_cast", "return", "short", "signed",
    "sizeof", "static", "static_assert", "static_cast", "struct",
    "switch", "template", "this", "thread_local", "throw", "true",
    "try", "typedef", "typeid", "typename", "union", "unsigned",
    "using", "virtual", "void", "volatile", "wchar_t", "while",
    "xor", "xor_eq",

    # También incluimos palabras comunes en directivas de preprocesador
    "include", "define"
}


def read_code(path):
    """
    Lee el contenido de un archivo de código.

    Los archivos del dataset no tienen extensión .cpp,
    pero siguen siendo archivos de texto, así que Python
    puede abrirlos normalmente.
    """

    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        return file.read()


def remove_comments(code):
    """
    Elimina comentarios de C++.

    Quita:
    - comentarios de una línea: // comentario
    - comentarios de varias líneas: /* comentario */
    """

    # Elimina comentarios de una línea.
    code = re.sub(r"//.*", "", code)

    # Elimina comentarios de varias líneas.
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)

    return code


def tokenize_cpp(code):
    """
    Convierte el código C++ en una lista de tokens normalizados.

    Ejemplo:
    int suma = 10;

    Se transforma aproximadamente en:
    INT ID = NUMBER ;

    La idea es conservar la estructura general del código,
    pero evitar que nombres de variables o valores específicos
    afecten demasiado la comparación.
    """

    # Primero eliminamos comentarios.
    code = remove_comments(code)

    # Extraemos tokens usando una expresión regular.
    # Esta regex detecta:
    # - identificadores: variable, sumaTotal, main
    # - números: 10, 3.14
    # - operadores dobles: ==, !=, <=, >=, ++, --, &&, ||, <<, >>
    # - símbolos comunes: + - * / % = < > ( ) { } [ ] , ; : # .
    tokens = re.findall(
        r"[A-Za-z_][A-Za-z0-9_]*|\d+\.\d+|\d+|==|!=|<=|>=|\+\+|--|&&|\|\||<<|>>|[+\-*/%=<>(){}[\],;:#.]",
        code
    )

    normalized_tokens = []

    for token in tokens:
        lower_token = token.lower()

        # Si es palabra reservada de C++, la conservamos como token especial.
        # La pasamos a mayúsculas para distinguirla de identificadores normales.
        if lower_token in KEYWORDS:
            normalized_tokens.append(lower_token.upper())

        # Si es número, lo reemplazamos por NUMBER.
        elif re.fullmatch(r"\d+\.\d+|\d+", token):
            normalized_tokens.append("NUMBER")

        # Si es un identificador, lo reemplazamos por ID.
        # Así nombres como x, contador, resultado o sumaTotal se tratan igual.
        elif re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", token):
            normalized_tokens.append("ID")

        # Si es operador o símbolo, lo dejamos tal cual.
        else:
            normalized_tokens.append(token)

    return normalized_tokens


def preprocess_code_from_path(path):
    """
    Función principal para preprocesar un archivo de código.

    Recibe la ruta del archivo, lee el código, lo tokeniza
    y regresa la lista de tokens normalizados.
    """

    code = read_code(path)
    tokens = tokenize_cpp(code)
    return tokens


# Esta parte solo sirve para probar el archivo directamente.
# No afecta cuando importemos este módulo desde otros scripts.
if __name__ == "__main__":
    example_path = "data/dev/43096"

    tokens = preprocess_code_from_path(example_path)

    print("Cantidad de tokens:", len(tokens))
    print("Primeros 100 tokens:")
    print(tokens[:100])