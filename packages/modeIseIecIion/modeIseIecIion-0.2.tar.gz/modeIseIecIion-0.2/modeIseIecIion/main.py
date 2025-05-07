def unsupervised_learning():
    a = '''
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import silhouette_score

    # Load dataset
    # file_path = 'your_file.csv' # Replace with actual CSV file path
    # data = pd.read_csv("/Users/hussamuddin/Downloads/housing.csv")
    dataa = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000,
    75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck',
    'Hatchback', 'SUV']
    }
    # Create a DataFrame
    data = pd.DataFrame(dataa)
    # Drop fully empty rows
    data.dropna(how='all', inplace=True)
    # Identify columns
    numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = data.select_dtypes(exclude=[np.number]).columns.tolist()
    # Fill missing values safely (no inplace warnings)
    for col in numeric_cols:
        data[col] = data[col].fillna(data[col].mean())
    for col in categorical_cols:
        data[col] = data[col].fillna(data[col].mode()[0])
    # One-hot encode categoricals
    data_encoded = pd.get_dummies(data, columns=categorical_cols)
    # Scale numeric features
    scaler = StandardScaler()
    data_scaled = data_encoded.copy()
    data_scaled[numeric_cols] = scaler.fit_transform(data_scaled[numeric_cols])

    # Elbow Method to find optimal k
    wcss = []
    silhouette_scores = []
    max_k = min(10, len(data) - 1)  # Ensure max_k doesn't exceed dataset size - 1

    print("Calculating errors for different cluster counts:")
    print("k\tWCSS\t\tSilhouette Score")
    print("-" * 40)

    for i in range(2, max_k + 1):  # Start from 2 as silhouette score needs at least 2 clusters
        kmeans = KMeans(n_clusters=i, random_state=42, n_init=10)
        kmeans.fit(data_scaled)
        wcss.append(kmeans.inertia_)

        # Calculate silhouette score (lower error = better clustering)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(data_scaled, labels)
        silhouette_scores.append(silhouette_avg)

        print(f"{i}\t{kmeans.inertia_:.2f}\t\t{silhouette_avg:.4f}")

    # Auto-select optimal k based on silhouette score (higher is better)
    optimal_k = np.argmax(silhouette_scores) + 2  # +2 because we started from k=2

    # Plot Elbow Curve
    plt.figure(figsize=(12, 5))

    # WCSS Plot
    plt.subplot(1, 2, 1)
    plt.plot(range(2, max_k + 1), wcss, marker='o')
    plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
    plt.title('Elbow Method for Optimal k')
    plt.xlabel('Number of Clusters')
    plt.ylabel('WCSS (Inertia)')
    plt.grid(True)
    plt.legend()

    # Silhouette Score Plot
    plt.subplot(1, 2, 2)
    plt.plot(range(2, max_k + 1), silhouette_scores, marker='o')
    plt.axvline(x=optimal_k, color='r', linestyle='--', label=f'Optimal k={optimal_k}')
    plt.title('Silhouette Score Method')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Silhouette Score')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

    print(f"\nAutomatically selected optimal k = {optimal_k} (highest silhouette score)")

    # Fit KMeans with optimal k
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    y_predict = kmeans.fit_predict(data_scaled)

    # Add cluster labels to data
    data['Cluster'] = y_predict

    # Visualize first two features (with colors and centroids)
    x = data_scaled.values
    colors = ['blue', 'green', 'red', 'black', 'purple', 'orange', 'pink', 'cyan', 'brown', 'grey']
    plt.figure(figsize=(8, 6))
    for i in range(optimal_k):
        plt.scatter(x[y_predict == i, 0], x[y_predict == i, 1], s=100,
                   c=colors[i % len(colors)], label=f'Cluster {i+1}')
    plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1],
               s=300, c='yellow', label='Centroid')
    plt.title(f'Clusters Visualization (k={optimal_k})')
    plt.xlabel('Feature 1 (scaled)')
    plt.ylabel('Feature 2 (scaled)')
    plt.legend()
    plt.show()

    # Print cluster distribution
    print("Cluster distribution:")
    print(data['Cluster'].value_counts())'''
    print(a)

def supervised_learning():
    a = '''
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    from sklearn.model_selection import KFold, LeaveOneOut, cross_val_predict
    from sklearn.linear_model import LogisticRegression, LinearRegression
    from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, r2_score,
        roc_auc_score, roc_curve, confusion_matrix, ConfusionMatrixDisplay
    )
    from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    
    # Load Data
    path = input("Enter path to CSV file: ")
    df = pd.read_csv(path)
    
    # Target column
    target_col = input("Enter target column name: ")
    X = df.drop(columns=[target_col])
    y = df[target_col]
    
    # Detect problem type
    is_classification = y.nunique() <= 10 and y.dtype != 'float'
    
    # Encode target if classification
    if is_classification:
        le = LabelEncoder()
        y = le.fit_transform(y)
    
    # Choose model
    print("Choose model:\n1. Logistic Regression\n2. Linear Regression\n3. Decision Tree")
    model_choice = input("Enter 1/2/3: ")
    
    if model_choice == '1':
        model = LogisticRegression(max_iter=1000)
        model_name = "Logistic Regression"
    elif model_choice == '2':
        model = LinearRegression()
        model_name = "Linear Regression"
    elif model_choice == '3':
        model = DecisionTreeClassifier() if is_classification else DecisionTreeRegressor()
        model_name = "Decision Tree"
    else:
        raise ValueError("Invalid model choice")
    
    # Preprocessing pipeline
    num_features = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
    cat_features = X.select_dtypes(include=['object', 'category', 'bool']).columns.tolist()
    
    numeric_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='mean')),
        ('scaler', StandardScaler())
    ])
    
    categorical_pipeline = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('encoder', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    preprocessor = ColumnTransformer([
        ('num', numeric_pipeline, num_features),
        ('cat', categorical_pipeline, cat_features)
    ])
    
    pipeline = Pipeline([
        ('preprocess', preprocessor),
        ('model', model)
    ])
    
    # Cross-validation choice
    print("Choose cross-validation:\n1. K-Fold\n2. Leave-One-Out (LOOCV)")
    cv_choice = input("Enter 1 or 2: ")
    
    if cv_choice == '1':
        k = int(input("Enter number of folds (e.g. 5 or 10): "))
        cv = KFold(n_splits=k, shuffle=True, random_state=42)
    elif cv_choice == '2':
        cv = LeaveOneOut()
    else:
        raise ValueError("Invalid CV choice")
    
    # Cross-validated predictions
    y_pred = cross_val_predict(pipeline, X, y, cv=cv, method='predict')
    
    # Metrics
    print(f"\n=== {model_name} Performance ===")
    
    if is_classification:
        acc = accuracy_score(y, y_pred)
        prec = precision_score(y, y_pred, average='weighted', zero_division=0)
        rec = recall_score(y, y_pred, average='weighted', zero_division=0)
        print(f"Accuracy:  {acc:.4f}")
        print(f"Precision: {prec:.4f}")
        print(f"Recall:    {rec:.4f}")
    
        # Confusion Matrix
        print("\nConfusion Matrix:")
        cm = confusion_matrix(y, y_pred)
        print(cm)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm)
        disp.plot(cmap='Blues')
        plt.title("Confusion Matrix")
        plt.grid(False)
        plt.show()
    
        # ROC Curve if binary classification
        if len(np.unique(y)) == 2:
            y_proba = cross_val_predict(pipeline, X, y, cv=cv, method='predict_proba')[:, 1]
            auc = roc_auc_score(y, y_proba)
            fpr, tpr, _ = roc_curve(y, y_proba)
            print(f"ROC AUC:   {auc:.4f}")
            plt.plot(fpr, tpr, label=f"ROC curve (AUC = {auc:.2f})")
            plt.plot([0, 1], [0, 1], linestyle='--')
            plt.xlabel('False Positive Rate')
            plt.ylabel('True Positive Rate')
            plt.title('ROC Curve')
            plt.legend()
            plt.grid(True)
            plt.show()
    
    else:
        from sklearn.metrics import mean_absolute_error, mean_squared_error
    
        r2 = r2_score(y, y_pred)
        mae = mean_absolute_error(y, y_pred)
        mse = mean_squared_error(y, y_pred)
    
        print(f"R2 Score:           {r2:.4f}")
        print(f"Mean Absolute Error: {mae:.4f}")
        print(f"Mean Squared Error:  {mse:.4f}")'''
    print(a)

def bayesian():
    a = '''
    from pgmpy.models import DiscreteBayesianNetwork
    from pgmpy.factors.discrete import TabularCPD
    from pgmpy.inference import VariableElimination
    # Step 1: Define the structure of the Bayesian Network
    model = DiscreteBayesianNetwork([
    ('Burglary', 'Alarm'),
    ('Earthquake', 'Alarm'),
    ('Alarm', 'JohnCalls'),
    ('Alarm', 'MaryCalls')
    ])
    # Step 2: Define the CPDs (Conditional Probability Distributions)
    # P(Burglary)
    cpd_burglary = TabularCPD(variable='Burglary', variable_card=2,
    values=[[0.999], [0.001]])
    # P(Earthquake)
    cpd_earthquake = TabularCPD(variable='Earthquake', variable_card=2,
    values=[[0.998], [0.002]])
    # P(Alarm | Burglary, Earthquake)
    cpd_alarm = TabularCPD(
    variable='Alarm',
    variable_card=2,values=[
    [0.999, 0.71, 0.06, 0.05], # Alarm = False
    [0.001, 0.29, 0.94, 0.95] # Alarm = True
    ],
    evidence=['Burglary', 'Earthquake'],
    evidence_card=[2, 2]
    )
    # P(JohnCalls | Alarm)
    cpd_john = TabularCPD(
    variable='JohnCalls',
    variable_card=2,
    values=[
    [0.3, 0.9], # JohnCalls = False
    [0.7, 0.1] # JohnCalls = True
    ],
    evidence=['Alarm'],
    evidence_card=[2]
    )
    # P(MaryCalls | Alarm)
    cpd_mary = TabularCPD(
    variable='MaryCalls',
    variable_card=2,
    values=[
    [0.2, 0.99], # MaryCalls = False
    [0.8, 0.01] # MaryCalls = True
    ],
    evidence=['Alarm'],
    evidence_card=[2]
    )
    # Step 3: Add CPDs to the model
    model.add_cpds(cpd_burglary, cpd_earthquake, cpd_alarm, cpd_john, cpd_mary)
    # Step 4: Verify the model
    assert model.check_model(), "Model is incorrect"
    # Step 5: Perform inference
    inference = VariableElimination(model)
    # Query: What is the probability of a burglary given that both John and Mary called?
    result = inference.query(variables=['Burglary'], evidence={'JohnCalls': 1,
    'MaryCalls': 1})
    print(result)'''
    print(a)

def markov():
    a = '''
    import numpy as np
    # Define the states and transition matrix
    states = ["Red", "Blue"]
    transition_matrix = np.array([[0.5, 0.5], # From Red -> Red or Blue
    [0.5, 0.5]]) # From Blue -> Red or Blue

    # Function to simulate the Markov process
    def simulate_markov_process(initial_state, num_steps):
    current_state = initial_state
    state_sequence = [current_state]
    for _ in range(num_steps):
    if current_state == "Red":
    next_state = np.random.choice(states,

    p=transition_matrix[0])
    else:
    next_state = np.random.choice(states,

    p=transition_matrix[1])
    state_sequence.append(next_state)
    current_state = next_state
    return state_sequence
    # Simulate the process starting from "Red" and for 10 steps
    initial_state = "Red"
    num_steps = 10
    state_sequence = simulate_markov_process(initial_state, num_steps)
    # Output the sequence of states
    print(f"State sequence for {num_steps} steps starting from
    {initial_state}:")
    print(" -> ".join(state_sequence))'''
    print(a)

def minimax():
    a = '''
    import math
    def minimax(values, depth, index, is_maximizing, level=0):
        indent = "  " * level
        if depth == 0:
            print(f"{indent}Leaf node value: {values[index]}")
            return values[index]

        left = minimax(values, depth - 1, index * 2, not is_maximizing, level + 1)
        right = minimax(values, depth - 1, index * 2 + 1, not is_maximizing, level + 1)

        if is_maximizing:
            chosen = max(left, right)
            print(f"{indent}Max node: max({left}, {right}) = {chosen}")
        else:
            chosen = min(left, right)
            print(f"{indent}Min node: min({left}, {right}) = {chosen}")

        return chosen

    def is_power_of_two(n):
        return n and (n & (n - 1) == 0)

    def run_minimax():
        print("Welcome to the Minimax Evaluator!")

        leaf_input = input("Enter the leaf node values separated by spaces (must be power of 2): ")
        values = list(map(int, leaf_input.strip().split()))

        if not is_power_of_two(len(values)):
            print("Error: Number of leaf nodes must be a power of 2.")
            return

        root_type = input("Is the root node a 'max' or 'min'? ").strip().lower()
        if root_type not in ['max', 'min']:
            print("Error: Root node must be either 'max' or 'min'.")
            return

        is_maximizing = root_type == 'max'
        depth = int(math.log2(len(values)))

        print("\nEvaluating the tree...\n")
        result = minimax(values, depth, 0, is_maximizing)

        print("\nFinal result at the root node:", result)

    run_minimax()'''
    print(a)

def alpha_beta():
    a = '''
    import math

    def alpha_beta(values, depth, index, alpha, beta, is_maximizing, level=0):
        indent = "  " * level
        if depth == 0:
            print(f"{indent}Leaf node value: {values[index]}")
            return values[index]

        if is_maximizing:
            max_eval = float('-inf')
            print(f"{indent}Max node at depth {level}, Alpha: {alpha}, Beta: {beta}")
            for i in range(2):
                child_index = index * 2 + i
                eval = alpha_beta(values, depth - 1, child_index, alpha, beta, False, level + 1)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                print(f"{indent}  Max node updated: Value = {max_eval}, Alpha = {alpha}")
                if beta <= alpha:
                    print(f"{indent}  Pruned remaining branches (Beta cutoff)")
                    break
            return max_eval
        else:
            min_eval = float('inf')
            print(f"{indent}Min node at depth {level}, Alpha: {alpha}, Beta: {beta}")
            for i in range(2):
                child_index = index * 2 + i
                eval = alpha_beta(values, depth - 1, child_index, alpha, beta, True, level + 1)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                print(f"{indent}  Min node updated: Value = {min_eval}, Beta = {beta}")
                if beta <= alpha:
                    print(f"{indent}  Pruned remaining branches (Alpha cutoff)")
                    break
            return min_eval

    def is_power_of_two(n):
        return n and (n & (n - 1) == 0)

    def run_alpha_beta():
        print("Welcome to Alpha-Beta Pruning Evaluator!")

        leaf_input = input("Enter the leaf node values separated by spaces (must be power of 2): ")
        values = list(map(int, leaf_input.strip().split()))

        if not is_power_of_two(len(values)):
            print("Error: Number of leaf nodes must be a power of 2.")
            return

        root_type = input("Is the root node a 'max' or 'min'? ").strip().lower()
        if root_type not in ['max', 'min']:
            print("Error: Root node must be either 'max' or 'min'.")
            return

        is_maximizing = root_type == 'max'
        depth = int(math.log2(len(values)))

        print("\nEvaluating the tree with Alpha-Beta Pruning...\n")
        result = alpha_beta(values, depth, 0, float('-inf'), float('inf'), is_maximizing)

        print("\nFinal result at the root node:", result)

    run_alpha_beta()    '''
    print(a)

def CSP():
    a = '''
    from ortools.sat.python import cp_model

    from constraint import Problem, AllDifferentConstraint
    import itertools


    # 1. CSP on Maximizing a Math Equation: maximize x + 2y + 3z where 0 <= x,y,z <= 10 and x + y + z <= 10
    def math_optimization_csp():
        problem = Problem()
        problem.addVariables(["x", "y", "z"], range(11))
        problem.addConstraint(lambda x, y, z: x + y + z <= 10, ["x", "y", "z"])

        solutions = problem.getSolutions()
        max_val = -1
        best_solution = None
        for sol in solutions:
            val = sol["x"] + 2 * sol["y"] + 3 * sol["z"]
            if val > max_val:
                max_val = val
                best_solution = sol
        print("\n[1] Math Optimization CSP")
        print("Best solution:", best_solution, "with value:", max_val)


    # 2. CSP on N-Queens Problem
    def n_queens_csp(n=8):
        problem = Problem()
        cols = range(n)
        problem.addVariables(cols, cols)

        # Constraints: no same row, and no same diagonal
        for i in cols:
            for j in cols:
                if i < j:
                    problem.addConstraint(lambda a, b, i=i, j=j: a != b and abs(a - b) != abs(i - j), (i, j))

        solutions = problem.getSolutions()
        print(f"\n[2] N-Queens Problem (N={n})")
        print("Number of solutions:", len(solutions))
        if solutions:
            print("One solution:", solutions[0])


    # 3. CSP on Seating Problem: 4 people with preferences
    def seating_csp():
        people = ["Alice", "Bob", "Carol", "David"]
        seats = range(4)

        problem = Problem()
        problem.addVariables(people, seats)
        problem.addConstraint(AllDifferentConstraint())  # All must have unique seats

        # Alice doesn't want to sit next to Bob
        def not_next_to(a, b):
            return abs(a - b) > 1
        problem.addConstraint(not_next_to, ("Alice", "Bob"))

        # Carol wants to sit to the right of David
        def right_of(c, d):
            return c == d + 1
        problem.addConstraint(right_of, ("Carol", "David"))

        solutions = problem.getSolutions()
        print("\n[3] Seating Arrangement CSP")
        print("Number of solutions:", len(solutions))
        if solutions:
            print("One solution:", solutions[0])

    def timetable_fixed_times():
        model = cp_model.CpModel()

        # 3 classes, 3 times, 2 rooms → 6 total (time,room) slots
        classes = ["Math", "English", "Science"]
        times   = ["8AM", "10AM", "12PM"]
        rooms   = ["Room1", "Room2"]

        num_times = len(times)
        num_rooms = len(rooms)
        num_slots = num_times * num_rooms

        # 1) A single integer slot variable per class, in [0..5]
        slot_var = {
            cls: model.NewIntVar(0, num_slots - 1, f"slot_{cls}")
            for cls in classes
        }

        # 2) No two classes can share the exact same (time,room) slot
        model.AddAllDifferent(slot_var.values())

        # 3) Extract the time‐index from each slot: time = slot // num_rooms
        time_var = {
            cls: model.NewIntVar(0, num_times - 1, f"time_{cls}")
            for cls in classes
        }
        for cls in classes:
            model.AddDivisionEquality(time_var[cls], slot_var[cls], num_rooms)

        # 4) Pin each class to its required hour:
        #    Math @ 8AM, English @ 10AM, Science @ 12PM
        model.Add(time_var["Math"]   == times.index("10AM"))
        model.Add(time_var["English"]== times.index("10AM"))
        model.Add(time_var["Science"]== times.index("8AM"))

        # Solve and print
        solver = cp_model.CpSolver()
        status = solver.Solve(model)

        print("\n[4] Timetable with Fixed Class Times")
        if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
            for cls in classes:
                slot     = solver.Value(slot_var[cls])
                t_idx    = solver.Value(time_var[cls])
                r_idx    = slot % num_rooms
                print(f"{cls} at {times[t_idx]} in {rooms[r_idx]}")
        else:
            print("No valid timetable found.")



    '''
    print(a)

def advanced_CSP():
    a = '''
    import math
    import random
    from ortools.sat.python import cp_model

    class GridEnvironment:
        def __init__(self, size):
            self.size = size
            self.grid = [[0 for _ in range(size)] for _ in range(size)]
            self.start = (random.randint(0, size-1), random.randint(0, size-1))
            self.goal = (random.randint(0, size-1), random.randint(0, size-1))

        def solve_csp(self):
            model = cp_model.CpModel()
            x1, y1 = self.start
            x2, y2 = self.goal

            # Variables
            a = abs(x2 - x1)
            b = abs(y2 - y1)
            c = model.NewIntVar(0, self.size * 2, 'c')
            a_sq = model.NewIntVar(0, self.size**2, 'a_sq')
            b_sq = model.NewIntVar(0, self.size**2, 'b_sq')
            c_sq = model.NewIntVar(0, self.size**2, 'c_sq')

            # Constraints: Squaring terms using multiplication equality
            model.AddMultiplicationEquality(a_sq, [a, a])
            model.AddMultiplicationEquality(b_sq, [b, b])
            model.AddMultiplicationEquality(c_sq, [c, c])
            model.Add(c_sq == a_sq + b_sq)

            # Solve the model
            solver = cp_model.CpSolver()
            status = solver.Solve(model)

            if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
                return a, b, solver.Value(c)
            return a, b, math.sqrt(a**2 + b**2)  # Fallback to normal calculation

        def display(self):
            print(f"Start Position: {self.start}")
            print(f"Goal Position: {self.goal}")
            a, b, c = self.solve_csp()
            print(f"Calculated Distances: Base={a}, Height={b}, Hypotenuse={c:.2f}")

    # Simulation
    environment = GridEnvironment(10)
    environment.display()
    '''
    print(a)

def SVM():
    a = '''
    import sys
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from sklearn.model_selection import train_test_split, cross_val_score
    from sklearn.preprocessing import StandardScaler
    from sklearn.svm import SVC, SVR
    from sklearn.metrics import (
        accuracy_score, classification_report, confusion_matrix,
        mean_squared_error, mean_absolute_error, r2_score
    )

    def main():
        # 1. User inputs
        file_path = input("Enter path to your CSV data file: ")
        target_col = input("Enter the target column name: ")

        # 2. Load data
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"Error loading file: {e}")
            sys.exit(1)

        if target_col not in df.columns:
            print(f"Target column '{target_col}' not found in data.")
            sys.exit(1)

        print("\nData Info:")
        print(df.info())
        print("\nData Description:")
        print(df.describe(include='all'))

        # 3. Visualize missing values
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False)
        plt.title('Missing Value Heatmap')
        plt.show()

        # 3b. Feature distributions
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

        for col in numeric_cols:
            plt.figure()
            df[col].hist(bins=30)
            plt.title(f'Distribution of {col}')
            plt.xlabel(col)
            plt.ylabel('Frequency')
            plt.show()

        for col in categorical_cols:
            plt.figure()
            df[col].value_counts().plot(kind='bar')
            plt.title(f'Value Counts of {col}')
            plt.ylabel('Count')
            plt.show()

        # 4. Missing value handling
        # Numeric: mean imputation
        for col in numeric_cols:
            if df[col].isnull().sum() > 0:
                df[col].fillna(df[col].mean(), inplace=True)

        # Categorical: mode imputation
        for col in categorical_cols:
            if df[col].isnull().sum() > 0:
                mode = df[col].mode()
                if not mode.empty:
                    df[col].fillna(mode[0], inplace=True)
                else:
                    df[col].fillna('Unknown', inplace=True)

        # 5. Encoding
        df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

        # 6. Feature-target split & scaling
        X = df_encoded.drop(target_col, axis=1)
        y = df_encoded[target_col]

        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # 7. Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X_scaled, y, test_size=0.2, random_state=42
        )

        # 8. Determine problem type
        is_classification = False
        if y.dtype == 'object' or y.dtype.name == 'category':
            is_classification = True
        elif np.issubdtype(y.dtype, np.integer) and y.nunique() < 20:
            is_classification = True

        # 9. Model training
        if is_classification:
            print("\nDetected classification problem.")
            model = SVC(kernel='rbf', probability=True)
        else:
            print("\nDetected regression problem.")
            model = SVR(kernel='rbf')

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        # 10. Evaluation
        if is_classification:
            acc = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {acc:.4f}")
            print("\nClassification Report:")
            print(classification_report(y_test, y_pred))

            # Confusion matrix
            cm = confusion_matrix(y_test, y_pred)
            plt.figure(figsize=(6, 5))
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
            plt.title('Confusion Matrix')
            plt.xlabel('Predicted')
            plt.ylabel('Actual')
            plt.show()

            # Cross-validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='accuracy')
            print(f"5-Fold CV Accuracy Scores: {cv_scores}")
            print(f"Mean CV Accuracy: {cv_scores.mean():.4f}\n")
        else:
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            mae = mean_absolute_error(y_test, y_pred)
            r2 = r2_score(y_test, y_pred)
            print(f"RMSE: {rmse:.4f}")
            print(f"MAE: {mae:.4f}")
            print(f"R^2 Score: {r2:.4f}\n")

            # Predicted vs Actual plot
            plt.figure()
            plt.scatter(y_test, y_pred)
            plt.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=2)
            plt.xlabel('Actual')
            plt.ylabel('Predicted')
            plt.title('Actual vs Predicted')
            plt.show()

            # Cross-validation
            cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='neg_mean_squared_error')
            cv_rmse = np.sqrt(-cv_scores)
            print(f"5-Fold CV RMSE Scores: {cv_rmse}")
            print(f"Mean CV RMSE: {cv_rmse.mean():.4f}\n")

        print("Pipeline complete.")

    if __name__ == "__main__":
        main()
'''
