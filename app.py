from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Enhanced responses for different programming languages
RESPONSES = {
    'python': {
        'hello': 'print("Hello, World!")',
        'loop': 'for i in range(5):\n    print(i)',
        'function': 'def my_function():\n    return "Hello from function"',
        'class': 'class MyClass:\n    def __init__(self):\n        self.name = "MyClass"\n\n    def say_hello(self):\n        return f"Hello from {self.name}"',
        'list': 'my_list = [1, 2, 3, 4, 5]\nprint(my_list[0])  # Access first element\nmy_list.append(6)  # Add element',
        'dictionary': 'my_dict = {"name": "John", "age": 30}\nprint(my_dict["name"])  # Access value\nmy_dict["city"] = "New York"  # Add new key-value pair',
        'if': 'x = 10\nif x > 5:\n    print("x is greater than 5")\nelif x == 5:\n    print("x is 5")\nelse:\n    print("x is less than 5")',
        'try': 'try:\n    result = 10 / 0\nexcept ZeroDivisionError:\n    print("Cannot divide by zero")\nfinally:\n    print("This always executes")',
        'decorator': '@my_decorator\ndef my_function():\n    print("Hello from decorated function")\n\ndef my_decorator(func):\n    def wrapper():\n        print("Before function call")\n        func()\n        print("After function call")\n    return wrapper',
        'generator': 'def my_generator():\n    for i in range(5):\n        yield i\n\nfor num in my_generator():\n    print(num)',
        'lambda': 'square = lambda x: x * x\nprint(square(5))  # Output: 25',
        'list comprehension': 'numbers = [1, 2, 3, 4, 5]\nsquares = [x * x for x in numbers]\nprint(squares)  # Output: [1, 4, 9, 16, 25]',
        'file handling': 'with open("file.txt", "r") as file:\n    content = file.read()\n    print(content)',
        'module': 'import math\nprint(math.sqrt(16))  # Output: 4.0',
        'package': 'from mypackage import mymodule\nmymodule.my_function()'
    },
    'java': {
        'hello': 'public class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello, World!");\n    }\n}',
        'loop': 'for(int i = 0; i < 5; i++) {\n    System.out.println(i);\n}',
        'function': 'public static String myFunction() {\n    return "Hello from function";\n}',
        'class': 'public class MyClass {\n    private String name;\n\n    public MyClass() {\n        this.name = "MyClass";\n    }\n\n    public String sayHello() {\n        return "Hello from " + name;\n    }\n}',
        'array': 'int[] numbers = {1, 2, 3, 4, 5};\nSystem.out.println(numbers[0]);  // Access first element\nnumbers[0] = 10;  // Modify element',
        'list': 'List<String> names = new ArrayList<>();\nnames.add("John");\nnames.add("Jane");\nSystem.out.println(names.get(0));',
        'if': 'int x = 10;\nif (x > 5) {\n    System.out.println("x is greater than 5");\n} else if (x == 5) {\n    System.out.println("x is 5");\n} else {\n    System.out.println("x is less than 5");\n}',
        'try': 'try {\n    int result = 10 / 0;\n} catch (ArithmeticException e) {\n    System.out.println("Cannot divide by zero");\n} finally {\n    System.out.println("This always executes");\n}',
        'interface': 'interface MyInterface {\n    void myMethod();\n}\n\nclass MyClass implements MyInterface {\n    public void myMethod() {\n        System.out.println("Interface method implementation");\n    }\n}',
        'inheritance': 'class Animal {\n    void eat() {\n        System.out.println("Animal is eating");\n    }\n}\n\nclass Dog extends Animal {\n    void bark() {\n        System.out.println("Dog is barking");\n    }\n}',
        'enum': 'enum Day {\n    MONDAY, TUESDAY, WEDNESDAY,\n    THURSDAY, FRIDAY, SATURDAY, SUNDAY\n}\n\nDay today = Day.MONDAY;',
        'thread': 'class MyThread extends Thread {\n    public void run() {\n        System.out.println("Thread is running");\n    }\n}\n\nMyThread thread = new MyThread();\nthread.start();',
        'file handling': 'try (BufferedReader reader = new BufferedReader(new FileReader("file.txt"))) {\n    String line;\n    while ((line = reader.readLine()) != null) {\n        System.out.println(line);\n    }\n} catch (IOException e) {\n    e.printStackTrace();\n}',
        'package': 'package com.example;\n\npublic class MyClass {\n    // Class implementation\n}'
    },
    'c': {
        'hello': '#include <stdio.h>\n\nint main() {\n    printf("Hello, World!\\n");\n    return 0;\n}',
        'loop': 'for(int i = 0; i < 5; i++) {\n    printf("%d\\n", i);\n}',
        'function': 'char* myFunction() {\n    return "Hello from function";\n}',
        'struct': 'struct Person {\n    char name[50];\n    int age;\n};\n\nstruct Person person1;\nstrcpy(person1.name, "John");\nperson1.age = 30;',
        'array': 'int numbers[5] = {1, 2, 3, 4, 5};\nprintf("%d\\n", numbers[0]);  // Access first element\nnumbers[0] = 10;  // Modify element',
        'pointer': 'int x = 10;\nint *ptr = &x;\nprintf("%d\\n", *ptr);  // Access value through pointer\n*ptr = 20;  // Modify value through pointer',
        'if': 'int x = 10;\nif (x > 5) {\n    printf("x is greater than 5\\n");\n} else if (x == 5) {\n    printf("x is 5\\n");\n} else {\n    printf("x is less than 5\\n");\n}',
        'malloc': 'int *arr = (int*)malloc(5 * sizeof(int));\nif (arr != NULL) {\n    arr[0] = 1;\n    free(arr);  // Don\'t forget to free memory\n}',
        'file handling': 'FILE *file = fopen("file.txt", "r");\nif (file != NULL) {\n    char line[100];\n    while (fgets(line, sizeof(line), file)) {\n        printf("%s", line);\n    }\n    fclose(file);\n}',
        'typedef': 'typedef struct {\n    int x;\n    int y;\n} Point;\n\nPoint p1;\np1.x = 10;\np1.y = 20;',
        'union': 'union Data {\n    int i;\n    float f;\n    char str[20];\n};\n\nunion Data data;\ndata.i = 10;',
        'bitwise': 'int a = 5;  // 0101\nint b = 3;  // 0011\nint result = a & b;  // 0001 (1)\nprintf("%d\\n", result);',
        'preprocessor': '#define PI 3.14159\n#define SQUARE(x) ((x) * (x))\n\nprintf("%f\\n", SQUARE(PI));'
    },
    'cpp': {
        'hello': '#include <iostream>\n\nint main() {\n    std::cout << "Hello, World!" << std::endl;\n    return 0;\n}',
        'loop': 'for(int i = 0; i < 5; i++) {\n    std::cout << i << std::endl;\n}',
        'function': 'std::string myFunction() {\n    return "Hello from function";\n}',
        'class': 'class MyClass {\nprivate:\n    std::string name;\n\npublic:\n    MyClass() : name("MyClass") {}\n\n    std::string sayHello() {\n        return "Hello from " + name;\n    }\n};',
        'vector': 'std::vector<int> numbers = {1, 2, 3, 4, 5};\nstd::cout << numbers[0] << std::endl;  // Access first element\nnumbers.push_back(6);  // Add element',
        'string': 'std::string name = "John";\nstd::cout << name << std::endl;\nname += " Doe";  // Concatenate',
        'if': 'int x = 10;\nif (x > 5) {\n    std::cout << "x is greater than 5" << std::endl;\n} else if (x == 5) {\n    std::cout << "x is 5" << std::endl;\n} else {\n    std::cout << "x is less than 5" << std::endl;\n}',
        'try': 'try {\n    int result = 10 / 0;\n} catch (const std::exception& e) {\n    std::cout << "Error: " << e.what() << std::endl;\n}',
        'template': 'template <typename T>\nT max(T a, T b) {\n    return (a > b) ? a : b;\n}\n\nint result = max(5, 10);',
        'smart pointer': 'std::unique_ptr<int> ptr = std::make_unique<int>(10);\nstd::cout << *ptr << std::endl;',
        'lambda': 'auto square = [](int x) { return x * x; };\nstd::cout << square(5) << std::endl;',
        'namespace': 'namespace MyNamespace {\n    void myFunction() {\n        std::cout << "Hello from namespace" << std::endl;\n    }\n}\n\nMyNamespace::myFunction();',
        'file handling': 'std::ifstream file("file.txt");\nstd::string line;\nwhile (std::getline(file, line)) {\n    std::cout << line << std::endl;\n}\nfile.close();',
        'operator overloading': 'class Vector {\npublic:\n    Vector operator+(const Vector& other) {\n        Vector result;\n        result.x = x + other.x;\n        result.y = y + other.y;\n        return result;\n    }\nprivate:\n    int x, y;\n};'
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    data = request.json
    language = data.get('language', '').lower()
    question = data.get('question', '').lower()
    
    if language not in RESPONSES:
        return jsonify({'error': 'Unsupported language'}), 400
    
    # Enhanced keyword matching
    response = None
    for key in RESPONSES[language]:
        if key in question:
            response = RESPONSES[language][key]
            break
    
    if not response:
        response = f"Sorry, I don't have a specific answer for that question in {language}. Try asking about:\n- Hello World programs\n- Loops\n- Functions\n- Classes\n- Arrays/Lists\n- If statements\n- Try-catch blocks\n- Pointers (C/C++)\n- Vectors (C++)\n- Structs (C)\n- Templates (C++)\n- Smart Pointers (C++)\n- Lambda expressions\n- File handling\n- Memory management\n- Object-oriented concepts"
    
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True) 