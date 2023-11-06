import pandas as pd
import random

def compatibility_score(offers_A, demands_A, offers_B, demands_B):
    if len(offers_A) != len(demands_A) or len(offers_B) != len(demands_B) or len(offers_A) != len(offers_B):
        raise ValueError("Input vectors must be the same size")    
    total_compatibility = 0
    total_criteria = len(offers_A)

    max_abs_value = max(
                        max(
                            max(abs(x) for x in offers_A),
                            max(abs(x) for x in demands_A),
                        ),
                        max(
                            max(abs(x) for x in offers_B),
                            max(abs(x) for x in demands_B),
                        ),
                    )
    
    for i in range(total_criteria):
        compatibility_AB = max_abs_value - abs(offers_A[i] - demands_B[i])
        compatibility_BA = max_abs_value - abs(offers_B[i] - demands_A[i])
        
        total_compatibility += (compatibility_AB + compatibility_BA) / 2    
    
    score = (total_compatibility / total_criteria)*100/max_abs_value
    return score

def generate_dataset(num_line):    
    data = []
    
    for _ in range(num_line):
        #vector_length = random.randint(1, 20)# Generate a random vector length
        vector_length = 5# Generate a random vector length
                
        # Generate vectors to offers and demands to person A and person B
        offers_A = [random.randint(1, 100) for _ in range(vector_length)]
        demands_A = [random.randint(1, 100) for _ in range(vector_length)]
        offers_B = [random.randint(1, 100) for _ in range(vector_length)]
        demands_B = [random.randint(1, 100) for _ in range(vector_length)]
        
        score = compatibility_score(offers_A, demands_A, offers_B, demands_B)
        
        data.append([offers_A, demands_A, offers_B, demands_B, score])

    # Create DataFrame of pandas
    df = pd.DataFrame(data, columns=['offers_A', 'demands_A', 'offers_B', 'demands_B', 'compatibility_percent'])

    # Save the DataFrame as a CSV file
    df.to_csv('compatibility_dataset_len5.csv', index=False)

generate_dataset(3000)


# Ejemplo de uso de compatibility_score
#ofertas_A = [4,7,6,6,8]
#demandas_A = [5,7,8,6,7]
#ofertas_B = [5,2,8,6,7]
#demandas_B = [4,3,9,6,8]

#compatibility = compatibility_score(ofertas_A, demandas_A, ofertas_B, demandas_B)
#print(f"Porcentaje de compatibilidad: {compatibility:.2f}%")