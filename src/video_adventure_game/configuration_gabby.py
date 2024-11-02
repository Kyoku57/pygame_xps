import os
from clip import ClipResources
from scene import Scene, SceneResources

# Screen size
screen_size=(800,450)

# assets and cache
assets_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "assets")
cache_dir=os.path.join(os.path.dirname(os.path.realpath(__file__)), "cache")

# Clip inventory
clips = ClipResources(assets_dir,cache_dir)
clips.add("GAB_DORT", "PXL_20241102_124442799.TSR.mp4",0,3)
clips.add("RAPH_ENTRE", "PXL_20241102_124508854.TSR.mp4",0,10)
clips.add("GAB_DORT_ZOOM", "PXL_20241102_124530530.TSR.mp4",0,3)
clips.add("RAPH_REVEILLE_GENTIMENT", "PXL_20241102_124603774.TSR.mp4")
clips.add("RAPH_REVEILLE_FORT", "PXL_20241102_124635064.TSR.mp4",1,-1)
clips.add("GAB_LEVE_DOUX", "PXL_20241102_124716730.TSR.mp4")
clips.add("GAB_LEVE_FURY", "PXL_20241102_124803377.TSR.mp4",1,0)
clips.add("GAB_SALLE_DE_BAIN", "PXL_20241102_124915028.TSR.mp4")
clips.add("GAB_SALLE_DE_BAIN_SORTIE", "PXL_20241102_124948340.TSR.mp4",0,-0.2)
clips.add("GAB_SORT_ESCALIER", "PXL_20241102_125028870.TSR.mp4")
clips.add("GAB_ESCALIER_FRIGO", "PXL_20241102_125109552.TSR.mp4",1,0)
clips.add("GAB_DEVANT_FRIGO", "PXL_20241102_125247936.TSR.mp4")
clips.add("ZOOM_COMPOTE", "PXL_20241102_125304149.TSR.mp4",0,1)
clips.add("ZOOM_BANANE", "PXL_20241102_125315397.TSR.mp4",0,1)
clips.add("GAB_REFLECHI_FRIGO", "PXL_20241102_125331105.TSR.mp4",0,2)
clips.add("GAB_CHOISI_COMPOTE", "PXL_20241102_125515349.TSR.mp4")
clips.add("GAB_MANGE_COMPOTE", "PXL_20241102_125530418.TSR.mp4")
clips.add("GAB_FIN_COMPOTE", "PXL_20241102_125604652.TSR.mp4")
clips.add("GAB_CHOISI_BANANE", "PXL_20241102_125630244.TSR.mp4")
clips.add("GAB_PREND_BANANE", "PXL_20241102_125651593.TSR.mp4")
clips.add("GAB_MANGE_BANANE", "PXL_20241102_125702311.TSR.mp4")
clips.add("GAB_FINI_BANANE", "PXL_20241102_125717425.TSR.mp4")
clips.add("GAB_MONTE_ESCALIER", "PXL_20241102_125734039.TSR.mp4")
clips.add("GAB_VA_VERS_CHAMBRE", "PXL_20241102_125824270.TSR.mp4")
clips.add("GAB_SE_COUCHE", "PXL_20241102_125846406.TSR.mp4")
clips.add("GAB_A_FAIM", "PXL_20241102_130223286.TSR.mp4",1,8)
clips.add("GAB_DEMANDE_A_RAPH", "PXL_20241102_130339168.TSR.mp4")
clips.add("GAB_ALLER_J_AI_FAIM", "PXL_20241102_130651802.TSR.mp4")
clips.add("RAPH_MANGE_TA_MAIN", "PXL_20241102_130733424.TSR.mp4")
clips.add("RAPH_VA_FRIGO", "PXL_20241102_130858713.TSR.mp4")

# Create Scenes inventory
scene_resources = SceneResources()

scene_resources.add(Scene(clips, scene_id="REVEIL_DE_GAB", menu_start_time=8, menu_duration=6)\
    .add_clip("GAB_DORT")\
    .add_clip("RAPH_ENTRE")\
    .add_clip("GAB_DORT_ZOOM")
    .add_choice("REVEILLE_BRUTAL", "Réveiller fort !!", "REVEIL_FORT")\
    .add_choice("REVEILLE_DOUX", "Réveiller avec douceur", "REVEIL_DOUX"))

scene_resources.add(Scene(clips, "REVEIL_DOUX", 30, 10)\
    .add_clip("RAPH_REVEILLE_GENTIMENT")\
    .add_clip("GAB_LEVE_DOUX")\
    .add_clip("GAB_A_FAIM")\
    .add_clip("GAB_DEMANDE_A_RAPH")\
    .add_clip("GAB_ALLER_J_AI_FAIM")\
    .add_choice("MANGE_TA_MAIN", "Mange ta main", "MANGE_TA_MAIN")\
    .add_choice("DESCEND_EN_BAS", "Descends au frigo", "DESCEND_EN_BAS"))

scene_resources.add(Scene(clips, "REVEIL_FORT", 3, 3)\
    .add_clip("RAPH_REVEILLE_FORT")\
    .add_clip("GAB_LEVE_FURY")\
    .add_clip("GAB_SALLE_DE_BAIN")\
    .add_clip("GAB_SALLE_DE_BAIN_SORTIE")\
    .add_clip("GAB_SORT_ESCALIER")\
    .add_choice("DESCEND_EN_BAS", "Descends au frigo", "FRIGO"))

scene_resources.add(Scene(clips,"MANGE_TA_MAIN", 3, 3)\
    .add_clip("RAPH_MANGE_TA_MAIN")\
    .add_choice("GO_TO_DEPART", "Retour au lit", "REVEIL_DE_GAB"))

scene_resources.add(Scene(clips,"DESCEND_EN_BAS", 3, 3)\
    .add_clip("RAPH_VA_FRIGO")\
    .add_choice("DESCEND_EN_BAS", "Descends au frigo", "FRIGO"))

scene_resources.add(Scene(clips,"FRIGO", 23, 8)\
    .add_clip("GAB_ESCALIER_FRIGO")\
    .add_clip("GAB_DEVANT_FRIGO")\
    .add_clip("ZOOM_COMPOTE")\
    .add_clip("ZOOM_BANANE")\
    .add_clip("GAB_REFLECHI_FRIGO")\
    .add_choice("COMPOTE", "Manger de la compote", "COMPOTE")\
    .add_choice("BANANE", "Manger une banane", "BANANE"))

scene_resources.add(Scene(clips,"COMPOTE", 3, 3)\
    .add_clip("GAB_CHOISI_COMPOTE")\
    .add_clip("GAB_MANGE_COMPOTE")\
    .add_clip("GAB_FIN_COMPOTE")\
    .add_choice("RETOUR_CHAMBRE", "Manger de la compote", "RETOUR_CHAMBRE"))

scene_resources.add(Scene(clips,"BANANE", 3, 3)\
    .add_clip("GAB_CHOISI_BANANE")\
    .add_clip("GAB_PREND_BANANE")\
    .add_clip("GAB_MANGE_BANANE")\
    .add_clip("GAB_FINI_BANANE")\
    .add_choice("RETOUR_CHAMBRE", "Manger de la compote", "RETOUR_CHAMBRE"))

scene_resources.add(Scene(clips,"RETOUR_CHAMBRE", 3, 3)\
    .add_clip("GAB_MONTE_ESCALIER")\
    .add_clip("GAB_VA_VERS_CHAMBRE")\
    .add_clip("GAB_SE_COUCHE")\
    .add_choice("GO_TO_DEPART", "Retour au lit", "REVEIL_DE_GAB"))




# ------------------ CHECK -------------------------------

print("Check coherence with ...")
for scene_id,scene in scene_resources.scenes.items():
    scene.duration()
print(" ... durations: OK")

for scene_id,scene in scene_resources.scenes.items():
    for choice in scene.choices:
        scene_resources.get(choice.next_scene)
print(" ... scene in choice: OK")

print("EVERYTHING IS OK ! Good Game !")