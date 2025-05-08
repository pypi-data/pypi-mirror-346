from src.pytwincatparser.Twincat4024Strategy import Twincat4024Strategy
from src.pytwincatparser.Loader import Loader
from pathlib import Path 

strategy = Twincat4024Strategy()
loader = Loader(strategy)


loader.strategy = strategy



    #print(strategy.load_objects(Path("TwincatFiles\Base\FB_Base.TcPOU")))
    #print(strategy.load_objects(Path("TwincatFiles\Commands\ST_PmlCommand.TcDUT")))
    #print(strategy.load_objects(Path("TwincatFiles\TwincatPlcProject.plcproj")))

objects = loader.load_objects(Path(r"C:\Users\samue\Desktop\GIT\test_twincat_doc\src\LCA_NGP_Core\LCA_NGP_Core.plcproj"))
for obj in objects:
    print(f"name:{obj.name} namespace:{obj.name_space} , parent:{obj.parent.name if obj.parent is not None else ""}, ident: {obj.get_identifier()}")