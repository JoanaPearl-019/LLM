def calculate(expression):
    try:
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error in calculation: {str(e)}"

# 🔽 Add this for testing
if __name__ == "__main__":
    expr = input("Enter a math expression: ")
    print(calculate(expr))
