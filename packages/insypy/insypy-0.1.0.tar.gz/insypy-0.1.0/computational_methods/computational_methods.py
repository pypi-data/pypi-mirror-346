import sympy
import numpy as np
from sympy import symbols, diff
import sympy as sp
import matplotlib.pyplot as plt
from typing import List, Tuple

def lagrange_multiplier(x_vals: List, y_vals: List, graph: bool = False, x_range: Tuple = (-10, 10)):
    """
    Ստանում է Լագրանժի միջարկվող բազմանդմաը

    :param x_vals: x արժեքների ցուցակ (կետեր)։
    :param y_vals: ֆունկցիայի արժեքների ցուցակ տրված կետերում։
    :param graph: Ցուցադրել ֆունկցիայի գրաֆիկը:
    :param x_range: Ցուցադրման միջակայքը։
    :return: Լագրանջի ինտերպոլացիոն բազմանդամը՝ որպես sympy.Expr տիպի օբյեկտ։
    """

    # Սիմվոլի սահմանում
    x = sp.symbols('x')
    n = len(x_vals)

    Pn = 0

    for i in range(n):
        L_i = 1
        for j in range(n):
            if j != i:
                L_i *= (x - x_vals[j]) / (x_vals[i] - x_vals[j])

        Pn += y_vals[i] * L_i
    Pn = sp.expand(Pn)

    if graph:
        # Հեղափոխում ենք sympy.Expr-ը numpy ֆունկցիայի
        f_lambdified = sp.lambdify('x', Pn, "numpy")

        # Ստեղծում ենք x-ների արժեքները
        x_values_for_graph = np.linspace(x_range[0], x_range[1], 400)
        y_values_for_graph = f_lambdified(x_values_for_graph)

        # Գծում ենք գրաֆիկը
        plt.plot(x_values_for_graph, y_values_for_graph, label=f'{str(Pn)}', color='b')

        # Գծում ենք սկզբնական կետերը
        plt.scatter(x_vals, y_vals, color='r', label="Տրված կետեր", zorder=5)  # Կարմիր կետեր

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Գրաֆիկ {str(Pn)}')
        plt.grid(True)
        plt.legend()
        plt.show()

    return Pn

def newton_interpolation(X, F, graph=False, x_range=(-10, 10)):
    """
    Հաշվարկում է Նյուտոնի ինտերպոլացիոն բազմանդամը տրված X և F կետերի համար:

    :param X: x արժեքների ցուցակ (կետեր)։
    :param F: ֆունկցիայի արժեքների ցուցակ տրված կետերում։
    :param graph: Ցուցադրել ֆունկցիայի գրաֆիկը:
    :param x_range: Ցուցադրման միջակայքը։
    :return: Նյուտոնի ինտերպոլացիոն բազմանդամը՝ որպես sympy.Expr տիպի օբյեկտ։
    """

    # Harmarutyun ֆունկցիա (համարկման տարբերակ)
    def harmarutyun(*args):
        if len(args) == 1:
            return args[0][1]
        else:
            x, f_x = zip(*args)
            return (harmarutyun(*args[1:]) - harmarutyun(*args[:-1])) / (x[-1] - x[0])

    # Նյուտոնի բազմանդամի հաշվարկ
    x = sp.symbols('x')
    N = F[0]
    X_F = [(X[i], F[i]) for i in range(len(X))]

    for i in range(1, len(X)):
        k = 1
        for j in range(i):
            k *= (x - X[j])
        k *= harmarutyun(*X_F[:i + 1])
        N += k

    # Նյուտոնի բազմանդամը պարզեցնել
    N = sp.simplify(N)

    if graph:
        # Հեղափոխում ենք sympy.Expr-ը numpy ֆունկցիայի
        f_lambdified = sp.lambdify('x', N, "numpy")

        # Ստեղծում ենք x-ների արժեքները
        x_values_for_graph = np.linspace(x_range[0], x_range[1], 400)
        y_values_for_graph = f_lambdified(x_values_for_graph)

        # Գծում ենք գրաֆիկը
        plt.plot(x_values_for_graph, y_values_for_graph, label=f'N: {str(N)}', color='b')

        # Գծում ենք սկզբնական կետերը
        plt.scatter(X, F, color='r', label="Original points", zorder=5)  # Կարմիր կետեր

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Graph of {str(N)}')
        plt.grid(True)
        plt.legend()
        plt.show()

    return N

def rectangular_method(f_str, a, b, n):
    """
    Ուղղանկյունների մեթոդը որոշյալ ինտեգրալի համար, որտեղ ֆունկցիան տրվում է որպես սթրինգ։

    :param f_str: Ինտեգրվող ֆունկցիան որպես սթրինգ։
    :param a: Ինտեգրալը հաշվարկելու ներքևի սահման։
    :param b: Ինտեգրալը հաշվարկելու վերևի սահման։
    :param n: Միջակայքը բաժանող հատվածների քանակը։
    :return: Ինտեգրալի մոտավոր արժեքը։
    """

    x = sp.symbols('x')

    f_expr = sp.sympify(f_str)

    h = (b - a) / n

    integral_approx = 0
    for i in range(n):
        x_i = a + i * h
        integral_approx += f_expr.subs(x, x_i)

    integral_approx *= h

    return integral_approx

def trapezoidal_method(f_str, a, b, n) -> float:
    """
    Սեղանների մեթոդը որոշյալ ինտեգրալի համար, որտեղ ֆունկցիան տրվում է որպես սթրինգ։

    :param f_str: Ինտեգրվող ֆունկցիան որպես սթրինգ։
    :param a: Ինտեգրալը հաշվարկելու ներքևի սահման։
    :param b: Ինտեգրալը հաշվարկելու վերևի սահման։
    :param n: Միջակայքը բաժանող հատվածների քանակը։
    :return: Ինտեգրալի մոտավոր արժեքը։
    """

    # Ստեղծում ենք sympy փոփոխականը
    x = sp.symbols('x')

    # Պարադոքս է, որ ֆունկցիան տրվում է որպես սթրինգ, ուստի այն պետք է փոխակերպել sympy-ի արտահայտության
    f_expr = sp.sympify(f_str)

    # Հարաբերակցություն (հանդիպման լայնություն)
    h = (b - a) / n

    # Հաշվում ենք սեղանների մեթոդի օգտագործմամբ ինտեգրալի մոտավորությունը
    integral_approx = (f_expr.subs(x, a) + f_expr.subs(x, b)) / 2

    for i in range(1, n):
        x_i = a + i * h
        integral_approx += f_expr.subs(x, x_i)

    # Վերջնական արդյունքը
    integral_approx *= h
    return float(integral_approx)

def parabola_method(f_str, a, b, n):
    """
    Պարաբոլների մեթոդը որոշյալ ինտեգրալի համար, որտեղ ֆունկցիան տրվում է որպես սթրինգ։

    :param f_str: Ինտեգրվող ֆունկցիան որպես սթրինգ։
    :param a: Ինտեգրալը հաշվարկելու ներքևի սահման։
    :param b: Ինտեգրալը հաշվարկելու վերևի սահման։
    :param n: Միջակայքը բաժանող հատվածների քանակը (պետք է լինի զույգ թիվ)։
    :return: Ինտեգրալի մոտավոր արժեքը։
    """

    if n % 2 != 0:
        raise ValueError("n պետք է լինի զույգ թիվ")

    # Ստեղծում ենք sympy փոփոխականը
    x = sp.symbols('x')

    # Պարադոքս է, որ ֆունկցիան տրվում է որպես սթրինգ, ուստի այն պետք է փոխակերպել sympy-ի արտահայտության
    f_expr = sp.sympify(f_str)

    # Հարաբերակցություն (հանդիպման լայնություն)
    h = (b - a) / n

    # Հաշվում ենք պարաբոլների մեթոդի օգտագործմամբ ինտեգրալի մոտավորությունը
    integral_approx = f_expr.subs(x, a) + f_expr.subs(x, b)

    # Զույգ և կենտ կետերը հաշվելու համար
    for i in range(1, n, 2):  # odd indices (4 * f(x_i))
        x_i = a + i * h
        integral_approx += 4 * f_expr.subs(x, x_i)

    for i in range(2, n, 2):  # even indices (2 * f(x_i))
        x_i = a + i * h
        integral_approx += 2 * f_expr.subs(x, x_i)

    # Վերջնական արդյունքը
    integral_approx *= h / 3
    return float(integral_approx)

def romberg_method(f_str, a, b, n, graph=False):
    """
    Ռոմբերգի մեթոդը որոշյալ ինտեգրալի համար, որտեղ ֆունկցիան տրվում է որպես սթրինգ։

    :param f_str: Ինտեգրվող ֆունկցիան որպես սթրինգ։
    :param a: Ինտեգրալը հաշվարկելու ներքևի սահման։
    :param b: Ինտեգրալը հաշվարկելու վերևի սահման։
    :param n: Մակարդակների քանակը։
    :param graph: Եթե True է, գրաֆիկը կցուցադրվի, եթե False՝ ոչ։
    :return: Ինտեգրալի մոտավոր արժեքը։
    """

    # Ստեղծում ենք sympy փոփոխականը
    x = sp.symbols('x')

    # Ֆունկցիայի արտահայտությունը ստանալու համար
    f_expr = sp.sympify(f_str)

    # Ռոմբերգի սեղանի առաջին մակարդակ
    h = b - a
    R = [[(f_expr.subs(x, a) + f_expr.subs(x, b)) * h / 2]]  # Առաջին մակարդակ

    results = [R[0][0]]  # Պահպանելու ենք ամեն մակարդակի արդյունքը

    # Ռոմբերգի մեթոդը հետագա մակարդակներով
    for k in range(1, n):
        h /= 2
        # Խմբավորել սեղանի արժեքները
        temp_sum = sum(f_expr.subs(x, a + i * h) for i in range(1, 2 ** k, 2))
        R.append([None] * (k + 1))  # Ավելացնում ենք նոր շարքը, որպեսզի սեղանը ճիշտ չափսի լինի
        R[k][0] = (R[k - 1][0] / 2) + h * temp_sum
        results.append(R[k][0])  # Պահպանել առաջին սյունը (մոտավորությունը)

        # Ճշգրտման հաշվարկ
        for j in range(1, k + 1):
            R[k][j] = (4 ** j * R[k][j - 1] - R[k - 1][j - 1]) / (4 ** j - 1)

    # Վերջնական արդյունքը
    result = float(R[-1][-1])

    # Գրաֆիկի կառուցում, եթե graph=True է
    if graph:
        # Ճշգրիտ արժեքը (հաշված է իմաստով)
        exact_result = (b ** 3 - a ** 3) / 3

        # Գրաֆիկի կառուցում
        plt.plot(range(1, n + 1), results, label="Ռոմբերգի մոտեցումներ")
        plt.axhline(exact_result, color='red', linestyle='--', label="Ճշգրիտ արժեք")
        plt.xlabel('Մակարդակ')
        plt.ylabel('Մոտավոր արժեք')
        plt.title(f"Ռոմբերգի մեթոդի մոտեցումներ ֆունկցիայի '{f_str}' համար")
        plt.legend()
        plt.grid(True)
        plt.show()

    return result

def euler_method_with_string(f_str, t0, y0, h, n):
    """
        Էյլերի մեթոդը դիֆերենցիալ հավասարման համար, որտեղ աջ կողմի ֆունկցիան տրվում է որպես սթրինգ։

        :param f_str: Δ𝑦/Δ𝑡 ֆունկցիան որպես սթրինգ, կախված t և y փոփոխականներից։
        :param t0: Սկզբնական արժեքը t-ի համար։
        :param y0: Սկզբնական արժեքը y-ի համար։
        :param h: Քայլի երկարությունը։
        :param n: Քայլերի քանակը։
        :return: Երկու ցուցակ՝ t-ի արժեքները և համապատասխան y-ի արժեքները։
    """
    # Symbolic փոփոխականների սահմանում
    t, y = sp.symbols('t y')
    # String-ը փոխարկում ենք Sympy արտահայտության
    f_expr = sp.sympify(f_str)
    # Ստեղծում ենք թվային ֆունկցիա՝ հաշվելու համար
    f_numeric = sp.lambdify((t, y), f_expr, "numpy")

    t_values = [t0]
    y_values = [y0]

    t_curr, y_curr = t0, y0
    for _ in range(n):
        y_curr = y_curr + h * f_numeric(t_curr, y_curr)
        t_curr = t_curr + h
        t_values.append(t_curr)
        y_values.append(y_curr)

    return t_values, y_values

def gauss_elimination(A, b):
    """
    Գաուսի մեթոդով գծային հավասարումների համակարգի լուծում։

    :param A: Գծային հավասարումների մատրից։
    :param b: Աջ կողմի վեկտոր։
    :return: Գծային հավասարումների համակարգի լուծումը։
    """

    n = len(b)
    # Ստեղծում ենք ընդլայնված մատրիցը
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

    # Forward elimination (եռանկյունաձև մատրիցի ստացում)
    for i in range(n):
        # Pivoting՝ եթե հիմնական տարրը զրո է, փոխել տողերը
        if augmented_matrix[i, i] == 0:
            for k in range(i + 1, n):
                if augmented_matrix[k, i] != 0:
                    augmented_matrix[[i, k]] = augmented_matrix[[k, i]]
                    break

        # Կարգաբերում հիմնական տողի տարրերը
        for j in range(i + 1, n):
            ratio = augmented_matrix[j, i] / augmented_matrix[i, i]
            augmented_matrix[j, i:] -= ratio * augmented_matrix[i, i:]

    # Back substitution (հետադարձ քայլ)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (augmented_matrix[i, -1] - np.dot(augmented_matrix[i, i + 1:n], x[i + 1:])) / augmented_matrix[i, i]

    return x

def gauss_jordan(A, b):
    """
    Գաուս-Ժորդանի մեթոդով գծային հավասարումների համակարգի լուծում։

    :param A: Գծային հավասարումների մատրից։
    :param b: Աջ կողմի վեկտոր։
    :return: Գծային հավասարումների համակարգի լուծումը։
    """

    n = len(b)
    # Ստեղծում ենք ընդլայնված մատրիցը
    augmented_matrix = np.hstack((A, b.reshape(-1, 1)))

    # Գործընթացը
    for i in range(n):
        # Pivoting (ապահովում ենք, որ հիմնական տարրը 0 չէ)
        if augmented_matrix[i, i] == 0:
            for k in range(i + 1, n):
                if augmented_matrix[k, i] != 0:
                    augmented_matrix[[i, k]] = augmented_matrix[[k, i]]
                    break

        # Normalize row by the pivot element
        augmented_matrix[i] = augmented_matrix[i] / augmented_matrix[i, i]

        # Զրոյացնում ենք բոլոր տարրերը հիմնական տարրի վերևում և ներքևում
        for j in range(n):
            if j != i:
                augmented_matrix[j] -= augmented_matrix[j, i] * augmented_matrix[i]

    # Վերադարձնում ենք լուծումները (վերջին սյունը՝ x)
    return augmented_matrix[:, -1]

def simple_iteration(A, b, x0, tol=1e-6):
    """
    Հասարակ իտերացիաների մեթոդ։

    :param A: numpy.ndarray, համակարգի մատրից։
    :param b: numpy.ndarray, ազատ անդամների վեկտոր։
    :param x0: numpy.ndarray, սկզբնական մոտարկում։
    :param tol: float, սխալի թույլատրելի շեմ (նախնական արժեքը՝ 1e-6)։
    :return: Լուծման վեկտոր և իտերացիաների քանակը։
    """

    M = np.diag(np.diag(A))  # Արտահանում ենք A-ի անկյունագծային մասը
    N = A - M  # Մնացած մասը

    M_inv = np.linalg.inv(M)  # M-ի հակադարձ մատրիցը

    x = x0.copy()
    iteration = 0
    while True:
        x_new = M_inv @ (b - N @ x)
        iteration += 1
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:  # Սխալի ստուգում
            return x_new
        x = x_new

def gauss_seidel_with_dvu(A, b, x0=None, tol=1e-10):
    """
        Զեյդելի մեթոդ, հիմնված մատրիցների (A = D + V + U) բաժանման վրա։

        :param A: ndarray, Գծային հավասարումների համակարգի (n times n) մատրիցը։
        :param b: ndarray, Աջ մասի վեկտորը։
        :param x0: ndarray, Սկզբնական մոտարկումը (եթե None, ապա զրոներով վեկտոր)։
        :param tol: float, Ճշգրտության շեմը կոնվերգման համար։
        :return: x (ndarray), Վերջնական լուծումը։
        :return: iter_count (int), Կատարված իտերացիաների քանակը։
    """

    n = len(b)
    x = np.zeros(n) if x0 is None else x0.copy()

    # Մատրիցների բաժանում A = D + V + U
    D = np.diag(np.diag(A))  # Գլխավոր անկյունագծային մատրից
    V = np.tril(A, k=-1)  # Ստորին եռանկյուն (առանց անկյունագծի)
    U = np.triu(A, k=1)  # Վերին եռանկյուն (առանց անկյունագծի)

    # Նախահաշվարկ D^-1
    D_inv = np.linalg.inv(D)

    iter_count = 0

    while True:
        iter_count += 1

        x_new = -np.dot(D_inv, np.dot(V + U, x)) + np.dot(D_inv, b)

        # Կոնվերգման ստուգում (∞-նորմա)
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            return x_new
        x = x_new

def leverrier_characteristic_polynomial(matrix):
    """
    Հաշվում է մատրիցի սեփական բազմանդամը Լևերեյի մեթոդով։

    :param matrix: numpy.ndarray, քառակուսի մատրից (n x n)։
    :return: list, սեփական բազմանդամի գործակիցները [c_n, c_{n-1}, ..., c_0]։
    """

    n = matrix.shape[0]
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Մատրիցը պետք է լինի քառակուսի:")

    # Սկզբնական պայմաններ
    coefficients = [0] * (n + 1)  # Սեփական բազմանդամի գործակիցները
    coefficients[-1] = 1  # c_n = 1
    B = np.eye(n)  # Սկսում ենք միավորային մատրիցից

    # Ռեկուրսիա
    for k in range(1, n + 1):
        # Հաշվում ենք S_k = trace(A * B)
        S_k = np.trace(matrix @ B)
        coefficients[-k - 1] = -S_k / k  # Գործակիցը

        # Թարմացնում ենք B-ն
        B = matrix @ B + coefficients[-k - 1] * np.eye(n)

    return coefficients

def faddeev_method(matrix):
    """
    Հաշվում է մատրիցի սեփական բազմանդամը Ֆադևի մեթոդով։

    :param matrix: numpy.ndarray, քառակուսի մատրից (n x n)։
    :return: list, սեփական բազմանդամի գործակիցները [c_n, c_{n-1}, ..., c_0]։
    """

    n = matrix.shape[0]
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Մատրիցը պետք է լինի քառակուսի:")

    # Սկզբնական պայմաններ
    coefficients = [0] * (n + 1)  # Սեփական բազմանդամի գործակիցները
    coefficients[-1] = 1  # c_n = 1
    B = np.eye(n)  # Սկսում ենք միավորային մատրիցից

    # Ռեկուրսիա
    for k in range(1, n + 1):
        # Հաշվում ենք trace(A * B)
        trace_value = np.trace(matrix @ B)
        coefficients[-k - 1] = trace_value / k  # Գործակիցը

        # Թարմացնում ենք B-ն
        B = matrix @ B - coefficients[-k - 1] * np.eye(n)
        print(B, )

    return coefficients

def von_mises_method(matrix, tol=1e-6, max_iter=1000):
    """
    Հաշվում է մատրիցի մոդուլով ամենամեծ սեփական արժեքը և համապատասխան սեփական վեկտորը
    Ֆոն Միզեսի մեթոդով:

    :param matrix: numpy.ndarray, քառակուսի մատրից (n x n)
    :param tol: float, ընդունելի շեղման սահման (ստուգում է զուգորդումը)
    :param max_iter: int, առավելագույն կրկնությունների թիվ
    :return: tuple, (մոդուլով ամենամեծ սեփական արժեքը, համապատասխան սեփական վեկտորը)
    """
    n = matrix.shape[0]
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Մատրիցը պետք է լինի քառակուսի:")

    # Սկզբնական պատահական ոչ զրոյական վեկտոր
    b_k = np.random.rand(n)
    b_k = b_k / np.linalg.norm(b_k)  # Նորմավորում

    lambda_old = 0  # Նախնական մոտավորում

    for _ in range(max_iter):
        # Հաշվում է նոր վեկտորը
        b_k1 = np.dot(matrix, b_k)
        b_k1_norm = np.linalg.norm(b_k1)
        b_k = b_k1 / b_k1_norm  # Նորմավորում

        # Գնահատում ենք սեփական արժեքը
        lambda_new = np.dot(b_k.T, np.dot(matrix, b_k))

        # Ստուգում ենք զուգորդումը
        if np.abs(lambda_new - lambda_old) < tol:
            break
        lambda_old = lambda_new

    return lambda_new, b_k

def newton_method_sympy(f_str, x0, tol=1e-3, max_iter=100):
    """
    Նյուտոնի մեթոդով լուծում է ոչ գծային հավասարումը f(x) = 0 `sympy`-ի միջոցով, որտեղ f(x) արտահայտությունն առաջանում է որպես string:

    :param f_str: ֆունկցիան f(x) որպես string (օրինակ՝ 'x**2 - 2')
    :param x0: սկզբնական մոտավորություն
    :param tol: սխալի թույլատրելի չափը
    :param max_iter: առավելագույն վերադարձումների քանակ
    :return: արմատը
    """
    x = sp.symbols('x')
    f = sp.sympify(f_str)  # Խմբագրում ենք string-ը որպես sympy արտահայտություն
    f_prime = sp.diff(f, x)  # ֆունկցիայի առաջին բաշխումը

    x_n = x0
    for i in range(max_iter):
        fx = f.subs(x, x_n)
        dfx = f_prime.subs(x, x_n)
        if abs(fx) < tol:
            return float(x_n)  # Եթե սխալը փոքր է թույլատրելի չափից, վերադարձնում ենք արդյունքը

        if dfx == 0:
            raise ValueError("Ֆունկցիայի առաջին բաշխումը հավասար է զրոյին, որը թույլատրված չէ")

        x_n = x_n - fx / dfx  # Նյուտոնի հանհասերությունը

    raise ValueError("Նյուտոնի մեթոդը չի գտել արմատը մինչև առավելագույն շրջադարձի քանակը")

def newton_method_system(equations: list[str], variables: list[str], initial_guess: list,
                         iterations=10, show_iteration_results=False):
    """
    Լուծում է հավասարումների համակարգ Նյուտոնի մեթոդով։

    :param show_iteration_results: Ցուցադրում է յուրաքանչյուր իտերացիայում փոփոխականների ընթացիկ արժեքը:
    :param equations: Հավասարումների համակարգի սյունակ-վեկտոր (բոլոր տողերը սթրինգ են)։
    :param variables: Փոփոխականների անունների ցուցակ (սթրինգերի ցուցակ)։
    :param initial_guess: Սկզբնական կետը (ցուցակ)։
    :param iterations: Իտերացիաների թիվը։
    :return: Ստացված արմատների ցուցակ։
    """

    # Փոփոխականների ստեղծում
    variables = symbols(variables)

    # Հավասարումների ցուցակի ստեղծում
    equations = [sympy.sympify(eq_str) for eq_str in equations]

    # Սկզբնական կետի numpy array
    x_current = np.array(initial_guess, dtype=float).reshape(-1, 1)

    # Հաշվում ենք ամեն կրկնողության համար
    for _ in range(iterations):
        # Գտնում ենք ֆունկցիաների արժեքները
        f_values = np.array([
            [float(eq.subs({var: x_current[i][0] for i, var in enumerate(variables)}))]
            for eq in equations
        ])
        print(f_values)

        # Հաշվում է Յակոբի մատրիցը
        jacobian = np.array([
            [
                float(diff(eq, var).subs({v: x_current[i][0] for i, v in enumerate(variables)}))
                for var in variables
            ]
            for eq in equations
        ])

        # Գտնում ենք Յակոբի մատրիցի հակադարձը
        jacobian_inv = np.linalg.inv(jacobian)

        # Թարմացնում ենք x_current-ը
        x_current = x_current - np.matmul(jacobian_inv, f_values)
        if show_iteration_results:
            for i in range(len(variables)):
                for j in range(len(variables)):
                    print(f"{i + 1}-րդ իտերացիայում {variables[j]} = {x_current[j]}")
                print()

    result = [float(x_current[i]) for i in range(len(x_current))]

    return result
