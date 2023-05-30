norm_cfg = dict(type='SyncBN', requires_grad=True)
model = dict(
    type='EncoderDecoder',
    pretrained='pretrain/mit_b5.pth',
    backbone=dict(
        type='MixVisionTransformer',
        in_channels=3,
        embed_dims=64,
        num_stages=4,
        num_layers=[3, 6, 40, 3],
        num_heads=[1, 2, 5, 8],
        patch_sizes=[7, 3, 3, 3],
        sr_ratios=[8, 4, 2, 1],
        out_indices=(0, 1, 2, 3),
        mlp_ratio=4,
        qkv_bias=True,
        drop_rate=0.0,
        attn_drop_rate=0.0,
        drop_path_rate=0.1),
    decode_head=dict(
        type='SegformerHead',
        in_channels=[64, 128, 320, 512],
        in_index=[0, 1, 2, 3],
        channels=256,
        dropout_ratio=0.1,
        num_classes=16,
        norm_cfg=dict(type='SyncBN', requires_grad=True),
        align_corners=False,
        loss_decode=dict(
            type='CrossEntropyLoss', use_sigmoid=False, loss_weight=1.0)),
    train_cfg=dict(),
    test_cfg=dict(mode='whole'))
dataset_type = 'CustomDataset'
data_root = '/ofo-share/repos-david/data/mmseg-training/safeforest23'
classes = ('Dry Grass', 'Green Grass', 'Dry Shrubs', 'Green Shrubs', 'Canopy',
           'Wood Pieces', 'Litterfall', 'Timber Litter', 'Live Trunks',
           'Bare Earth', 'People', 'Sky', 'Blurry', 'Obstacles')
img_norm_cfg = dict(
    mean=[71.27821354460872, 70.71086780697692, 71.91041988796658],
    std=[32.98343261843338, 31.74368632485595, 32.66905186610359],
    to_rgb=True)
crop_size = (256, 512)
train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(type='Resize', img_scale=(848, 480), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=(256, 512), cat_max_ratio=0.75),
    dict(type='RandomFlip', prob=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(
        type='Normalize',
        mean=[71.27821354460872, 70.71086780697692, 71.91041988796658],
        std=[32.98343261843338, 31.74368632485595, 32.66905186610359],
        to_rgb=True),
    dict(type='Pad', size=(256, 512), pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg'])
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(848, 480),
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(
                type='Normalize',
                mean=[71.27821354460872, 70.71086780697692, 71.91041988796658],
                std=[32.98343261843338, 31.74368632485595, 32.66905186610359],
                to_rgb=True),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img'])
        ])
]
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type='CustomDataset',
        data_root='/ofo-share/repos-david/data/mmseg-training/safeforest23',
        img_dir='img_dir/train',
        ann_dir='ann_dir/train',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(type='LoadAnnotations'),
            dict(type='Resize', img_scale=(848, 480), ratio_range=(0.5, 2.0)),
            dict(type='RandomCrop', crop_size=(256, 512), cat_max_ratio=0.75),
            dict(type='RandomFlip', prob=0.5),
            dict(type='PhotoMetricDistortion'),
            dict(
                type='Normalize',
                mean=[71.27821354460872, 70.71086780697692, 71.91041988796658],
                std=[32.98343261843338, 31.74368632485595, 32.66905186610359],
                to_rgb=True),
            dict(type='Pad', size=(256, 512), pad_val=0, seg_pad_val=255),
            dict(type='DefaultFormatBundle'),
            dict(type='Collect', keys=['img', 'gt_semantic_seg'])
        ],
        img_suffix='_rgb.png',
        seg_map_suffix='_segmentation.png',
        classes=('Dry Grass', 'Green Grass', 'Dry Shrubs', 'Green Shrubs',
                 'Canopy', 'Wood Pieces', 'Litterfall', 'Timber Litter',
                 'Live Trunks', 'Bare Earth', 'People', 'Sky', 'Blurry',
                 'Obstacles')),
    val=dict(
        type='CustomDataset',
        data_root='/ofo-share/repos-david/data/mmseg-training/safeforest23',
        img_dir='img_dir/val',
        ann_dir='ann_dir/val',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(848, 480),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[
                            71.27821354460872, 70.71086780697692,
                            71.91041988796658
                        ],
                        std=[
                            32.98343261843338, 31.74368632485595,
                            32.66905186610359
                        ],
                        to_rgb=True),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ],
        img_suffix='_rgb.png',
        seg_map_suffix='_segmentation.png',
        classes=('Dry Grass', 'Green Grass', 'Dry Shrubs', 'Green Shrubs',
                 'Canopy', 'Wood Pieces', 'Litterfall', 'Timber Litter',
                 'Live Trunks', 'Bare Earth', 'People', 'Sky', 'Blurry',
                 'Obstacles')),
    test=dict(
        type='CustomDataset',
        data_root='/ofo-share/repos-david/data/mmseg-training/safeforest23',
        img_dir='img_dir/test',
        ann_dir='ann_dir/test',
        img_suffix='_rgb.png',
        seg_map_suffix='_segmentation.png',
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(
                type='MultiScaleFlipAug',
                img_scale=(848, 480),
                flip=False,
                transforms=[
                    dict(type='Resize', keep_ratio=True),
                    dict(type='RandomFlip'),
                    dict(
                        type='Normalize',
                        mean=[
                            71.27821354460872, 70.71086780697692,
                            71.91041988796658
                        ],
                        std=[
                            32.98343261843338, 31.74368632485595,
                            32.66905186610359
                        ],
                        to_rgb=True),
                    dict(type='ImageToTensor', keys=['img']),
                    dict(type='Collect', keys=['img'])
                ])
        ],
        classes=('Dry Grass', 'Green Grass', 'Dry Shrubs', 'Green Shrubs',
                 'Canopy', 'Wood Pieces', 'Litterfall', 'Timber Litter',
                 'Live Trunks', 'Bare Earth', 'People', 'Sky', 'Blurry',
                 'Obstacles')))
log_config = dict(
    interval=50, hooks=[dict(type='TextLoggerHook', by_epoch=False)])
dist_params = dict(backend='nccl')
log_level = 'INFO'
load_from = None
resume_from = None
workflow = [('train', 1)]
cudnn_benchmark = True
optimizer = dict(
    type='AdamW',
    lr=6e-05,
    betas=(0.9, 0.999),
    weight_decay=0.01,
    paramwise_cfg=dict(
        custom_keys=dict(
            pos_block=dict(decay_mult=0.0),
            norm=dict(decay_mult=0.0),
            head=dict(lr_mult=10.0))))
optimizer_config = dict()
lr_config = dict(
    policy='poly',
    warmup='linear',
    warmup_iters=1500,
    warmup_ratio=1e-06,
    power=1.0,
    min_lr=0.0,
    by_epoch=False)
runner = dict(type='IterBasedRunner', max_iters=20000)
checkpoint_config = dict(by_epoch=False, interval=2000)
evaluation = dict(interval=2000, metric='mIoU', pre_eval=True)
work_dir = './work_dirs/segformer_mit-b5_512x512_20k_safeforest_over_canopy'
gpu_ids = range(0, 1)
