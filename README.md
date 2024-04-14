# Project Tour OSM
> CMPT 353 - E100 SPRING 2024 Final Project

An exploratory analysis to investigate the potential correlation between restaurant cuisine and the ethnic demographics of the local population.  

## Group 
| Name | Student Number | Git ID |
|------------------|----------------|-------------|
| Heorhii Shramko|301428235| ShayGeko |
| Eunsong Koh| 301549157 | eunsongkoh|
| Tianyu Liu |301249861|tla109|


## Prerequisties
To run this project, Python3 and the following libraries must be installed:

### Installing Python3:
Download and install Python3 from the [official website](https://www.python.org/downloads/).

### Installing Required Libraries:
- Pandas
- Numpy
- Pytorch
- Matplotlib
- Sentence_transformers
- Pyspark
- Tqdm
- Sklearn

You can install the required Python libraries using `pip`, Python's package installer. Open a terminal or command prompt and execute the following commands:

```bash
pip3 install torch pandas numpy matplotlib pyyaml tqdm scikit-learn
```

## Run 
  ### Step 1. Clone the Repository 
  ```
  git clone git@github.com:ShayGeko/ProjectTourOSM.git
  ```
  ```  
  cd ProjectTourOSM
  ```

  ### Step 2. (Optional) Generate Embeddings:
  Gets the data from ```./bingMaps/restaurantCategory/``` and produce ```./embeddings/pca_category_bing_embeddings.csv```  
  and  ```./embeddingscategory_bing_embeddings.csv```
  
    
    python3 create_embeddings.py
    

  ### Step 3. Train on the Embeddings 
  1) Go to ```configs/ce_pca_category.yml``` and increment the counter in the ```name```  
    e.g. ```name: 'ce-category-embedding-1'``` -> ```name: 'ce-category-embedding-2'```

  2) From the root directory: 
    
    python3 train.py configs/ce_pca_category.yml
    

  will train with CrossEntropy loss on the PCA'd embeddings

If there was a problem with embedding generation (even though there shouldnt be 🙏), you can use the other embedding file for names instead of categories. Just change the config file in **Step 3** from ```ce_pca_category.yml``` to ```ce_pca_name.yml ```

Then one can observe results in under ```experiments/<experiment name from config file>/```
The predictions are stored every 1000 epochs under ```visuals/``` and the loss is plotted iteratively in ```loss.png```


  
  ### Data Visualizations 
  From the root directory:  
      ```python3 visualize.py <experiment name from config file>```

## [License](https://github.com/ShayGeko/ProjectTourOSM/blob/main/LICENSE)
MIT © [Heorhii Shramko](https://github.com/ShayGeko)
