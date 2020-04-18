from ahp import AHP

example = AHP(method='', precision=3, alternatives=['Tom', 'Dick', 'Harry'], 
              criteria=['Experiência', 'Educação', 'Carisma', 'Idade'], sub_criteria={},
              matrix={
                  'Experiência': [
                      [1, 1/4, 4],
                      [4, 1, 9],
                      [1/4, 1/9, 1]
                  ],
                  'Educação': [
                      [1, 3, 1/5],
                      [1/3, 1, 1/7],
                      [5, 7, 1]
                  ],
                  'Carisma': [
                      [1, 5, 9],
                      [1/5, 1, 4],
                      [1/9, 1/4, 1]
                  ],
                  'Idade': [
                      [1, 1/3, 5],
                      [3, 1, 9],
                      [1/5, 1/9, 1]
                  ],
                  'criterios': [
                      [1, 4, 3, 7],
                      [1/4, 1, 1/3, 3],
                      [1/3, 3, 1, 5],
                      [1/7, 1/3, 1/5, 1]
                  ]
              },
              log=True
            )

example.local_priorities()