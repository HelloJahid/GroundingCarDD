


# GroundingCarDD: Text-Guided Multimodal Phrase Grounding for Car Damage Detection  


The rising incidence of vehicle accidents and the rapid growth of online car marketplaces highlight the **critical need for efficient and accurate car damage inspection** in rental services, insurance claims processing, and vehicle maintenance.  

Traditional manual inspection methods are:  
- ⏳ Time-consuming  
- ❌ Error-prone  
- ⚠️ Vulnerable to fraud  

This underscores the necessity for **automated, reliable, and scalable solutions**.  

---

## 🔍 Limitations of Existing Methods  
Current automated object detection models:  
- Struggle to identify **minor damages** on car bodies  
- Fail to distinguish actual damage from **features, reflections, or shadows**  
- Lack effective methods for **feature extraction and contextual understanding**  

---

## 💡 Our Contribution: GroundingCarDD  
We introduce **GroundingCarDD**, a **text-guided multimodal phrase grounding framework** that leverages both **visual and textual information** to:  
- Precisely **localise and classify car damages**  
- Employ a **context-aware attention mechanism** to fuse features  
- Deliver superior performance over state-of-the-art methods  


## Model Architecture  

<p align="center">
  <img src="paper/GroundingCarDD Overall Model.jpg" alt="GroundingCarDD Architecture" width="600">
</p>



### Model Contributions  

1. **Expanded Dataset**  
   - Curated a private dataset and combined it with the public CarDD dataset  
   - Manually corrected bounding box annotations and added detailed image captions  
   - Improved detection accuracy for small damages in complex scenarios  

2. **Enhanced Image-Text Correlation**  
   - Introduced phrase grounding object detection to fuse **visual** and **textual** data  
   - Enabled better contextual understanding of damage by linking descriptions with visual regions  

3. **Improved Localization and Segmentation**  
   - Integrated the **Segment Anything Model 2 (SAM2)** with GroundingCarDD  
   - Achieved refined pixel-level segmentation of damaged areas within bounding boxes  
   - Distinguished between superficial and structural damages for better repair assessment  

4. **Custom Car-Specific Model Enhancements** ⚙️  
   - Developed **damage-specific feature extractors** using Swin Transformer for fine-grained details (scratches, dents, broken parts)  
   - Added **hierarchical feature aggregation** and **multi-scale fusion** with pyramid pooling to capture damage at different scales  

5. **Advanced Cross-Modal Attention Mechanisms** 🎯  
   - Designed **dynamic attention weights** to emphasise critical words in textual descriptions  
   - Applied **context-aware attention** that aligns text with relevant car regions, improving accuracy in challenging conditions  



⚠️ **Note:**  The **enhancement code** (including *Car-Specific Model Enhancements* and *Advanced Cross-Modal Attention Mechanisms*) is **available only upon request**. Please contact the authors if you wish to access it.  


---

## 📊 Key Results  
On a combined dataset of public and curated private data:  
- **mAP:** 64.1  
- **Miss Detection Rate:** 14.4%  
- Outperforms **YOLOv9** and **DETR**  

On the public **CarDD dataset**:  
- **AP50:** 80  
- **Recall:** 86.7  
- Surpasses all existing benchmark models  

---

## 🌍 Impact  
GroundingCarDD has the potential to transform the automotive industry by:  
- ✅ Enabling **automated and accurate car damage assessment**  
- ✅ Improving **insurance claims transparency**  
- ✅ Optimising **vehicle servicing**  
- ✅ Enhancing **trust in online car sales**  

Ultimately, this framework benefits **consumers, businesses, and the industry as a whole**.  

DOI: https://doi.org/10.1109/ACCESS.2024.3506563
<br><br>
---

# Installing GroundingCarDD

## 1. Clone this repository.
```bash
git clone https://github.com/HelloJahid/GroundingCarDD.git && cd GroundingCarDD/
```

## 2. Install the required dependencies.

```bash
pip install -r requirements.txt 
```

```bash
cd models/GroundingDINO/ops
python setup.py build install
```

```bash
python test.py
cd ../../..
```
## 3. Download Pretrained Weight 
### 3.1 Download BERT Base Uncased into Current Directory

```bash
sudo apt-get install git-lfs
```

```bash
git clone https://huggingface.co/google-bert/bert-base-uncased
```


### 3.2 Download pretrained gdino weight

```bash
wget https://github.com/IDEA-Research/GroundingDINO/releases/download/v0.1.0-alpha/groundingdino_swint_ogc.pth
```

# Dataset Format


## Label map

- In order to align with visual grounding(VG) data, we need to provide an additional mapping table for object detection(OD) data.
- In dictionary form, indices start from "0" (it is essential to start from 0 to accommodate caption/grounding data). 

```json
{"0": "wheel", "1": "carlight", "2" : "car"}
```


The files are in jsonl format, with one json object per line, as follows:
- Object Detection datasets utilize the ``detection`` field. If dealing with an Object Detection dataset, an additional ``label_map`` is required in the Dataset settings.
- Visual Grounding datasets employ the ``grounding`` field.  

```json
[
  {
    "filename": "car_001.jpg",
    "image_size": {
      "width": 512,
      "height": 512
    },
    "caption": "This image displays a car with key vehicle components such as carlights, wheels, and other body parts.",
    "objects": [
      {
        "bbox": [114.0, 231.0, 230.0, 247.0],
        "label": 1,
        "category": "carlight",
        "phrase": "Headlight, clearly visible on the car."
      },
      {
        "bbox": [382.0, 180.0, 405.0, 193.0],
        "label": 1,
        "category": "carlight",
        "phrase": "Rear car light, clearly visible on the car."
      },
      {
        "bbox": [63.0, 256.0, 163.0, 338.0],
        "label": 0,
        "category": "wheel",
        "phrase": "Noticeable wheel present on the car"
      },
      {
        "bbox": [1.0, 148.0, 503.0, 338.0],
        "label": 2,
        "category": "car",
        "phrase": "The car is clearly visible."
      },
      {
        "bbox": [278.0, 158.0, 501.0, 213.0],
        "label": 2,
        "category": "car",
        "phrase": "The car is clearly visible."
      }
    ]
  }
]
.
.
.
```



# Traning 

## Set data Path

- update custom data_path.json
```bash
rm config/data_path.json
nano config/data_path.json
```

- for train change only - root, anno, label_map used label.json 
- for valid change only - root, anno

```bash
{
  "train": [
    {
      "root": "path/images/train/",
      "anno": "path/annotations/train_annotations.jsonl",
      "label_map": "path/annotations/label_map.json",
      "dataset_mode": "odvg"
    }
  ],
  "val": [
    {
      "root": "path/images/valid",
      "anno": "path/annotations/valid_annotations.json",
      "label_map": null,
      "dataset_mode": "coco"
    }
  ]
}

```

## Train GroundingCarDD

```bash
nano train.sh
```

```bash
GPU_NUM=4

torchrun --nproc_per_node=${GPU_NUM} main.py \
    --output_dir /home/ubuntu/Open-GroundingDino/finetune_weight \
    -c config/cfg_odvg.py \
    --datasets config/data_path.json \
    --pretrain_model_path /home/ubuntu/Open-GroundingDino/groundingdino_swint_ogc.pth \
    --options text_encoder_type=/home/ubuntu/Open-GroundingDino/bert-base-uncased
```
```bash
chmod +x train.sh
./train.sh
```


---

## 🙏 Acknowledgements  

> Special thanks to the amazing open-source projects that inspired and supported this work:  
> - [GroundingDINO](https://github.com/IDEA-Research/GroundingDINO)  
> - [Open-GroundingDINO](https://github.com/longzw1997/Open-GroundingDino)  

Your contributions have made **GroundingCarDD** possible.  
