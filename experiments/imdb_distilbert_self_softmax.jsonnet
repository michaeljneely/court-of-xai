local batch_size = 64;
{
    "dataset_reader": {
        "type": "imdb_csv",
        "max_review_length": 240,
        "pretrained_tokenizer": "distilbert-base-uncased"
    },
    "train_data_path": std.join("/", [std.extVar("PWD"), "ane_research/datasets/IMDB/train.csv"]),
    "test_data_path": std.join("/", [std.extVar("PWD"), "ane_research/datasets/IMDB/test.csv"]),
    "validation_data_path": std.join("/", [std.extVar("PWD"), "ane_research/datasets/IMDB/dev.csv"]),
    "evaluate_on_test": false,
    "model": {
        "type": "distilbert_sequence_classification_from_huggingface",
        "model_name": "distilbert-base-uncased",
        "ffn_activation": "gelu",
        "ffn_dropout": 0.2,
        "attention": {
            "type": "multihead_self",
            "n_heads": 12,
            "dim": 768,
            "activation_function": {
                "type": "softmax"
            },
            "dropout": 0.2
        },
        "num_labels": 2,
        "seq_classif_dropout": 0.1
    },
    "data_loader": {
        "batch_sampler": {
            "type": "bucket",
            "batch_size": batch_size
        }
    },
    "trainer": {
        "num_epochs": 40,
        "patience": 5,
        "validation_metric": "+accuracy",
        "optimizer": {
            "type": "huggingface_adamw",
            "lr": 1.0e-5
        }
    },
    "attention_experiment": {
        "feature_importance_measures": [
            {
                "type": "leave-one-out"
            },
            // {
            //     "type": "lime",
            //     "num_samples": 250
            // },
            {
                "type": "captum",
                "captum": "captum-integrated-gradients"
            },
            {
                "type": "captum",
                "captum": "captum-deepliftshap"
            },
            {
                "type": "captum",
                "captum": "captum-gradientshap"
            },
            {
                "type": "captum",
                "captum": "captum-deeplift"
            }
        ],
        "correlation_measures": [
            {
                "type": "kendall_tau"
            },
            {
                "type": "kendall_top_k_average_length"
            }
        ],
        "dataset": "IMDb",
        "model": "DistilBERT",
        "compatibility_function": "Self",
        "activation_function": "Softmax",
        "batch_size": batch_size,
        "cuda_device": -1
    }
}