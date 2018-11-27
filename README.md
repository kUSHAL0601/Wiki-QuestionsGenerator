# Wiki-QuestionsGenerator
Final Poject for NLP course

# WORKFLOW
+ In the first stage we focus on over generating questions taking different answer phrases. We would first be focusing on generating the basic wh questions from the given corpus, as our initial goal. We will first be analysing the sentences and mark the unmovable phrases. We will then generate the possible question phrases for each answer phrase. We will then decompose the main verb and change the subject and predicate for question formation. As part of our next stage, we will also focus on anaphora resolution, I.e. replacing the pronouns with the nearest object.

+ As part of the second stage, we will generate feature vectors based on various features like grammatical features, N-Gram Language Model features, Vagueness, Pronoun Replacement etc. We will then train on these feature vectors, finding appropriate weights for the features and thus generating a score for each question. We will then proceed to rank these questions based on this score. We will try to do this basic work as a baseline.

+ As part of our next stage, we will try to implement the following features:
1. introduction of questions based on date tuples. It might require a bit of dataset training and we might try to do that if possible.
2. We will try to follow the SSF format in our workflow. It has been just taught so we cannot guarantee how well we can implement it.

# INSTRUCTIONS
+ Try to make your own branches for work, and merge it with master after checking there are no merge conflicts.

# FINAL WORK SLIDES
+ https://prezi.com/view/fSYQVKY82Lb1vXIDi3n9/
