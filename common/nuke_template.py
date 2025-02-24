def build_nuke_script_template(seq_name, shot_name, fps, width, height, resolution_label, use_proxy, use_aces):
    define_window_layout = """define_window_layout_xml {<?xml version="1.0" encoding="UTF-8"?>
<layout version="1.0">
    <window x="-1" y="-8" w="2560" h="1369" maximized="1" screen="0">
        <splitter orientation="1">
            <split size="53"/>
            <dock id="" hideTitles="1" activePageId="Toolbar.1">
                <page id="Toolbar.1"/>
            </dock>
            <split size="1895"/>
            <splitter orientation="2">
                <split size="1328"/>
                <dock id="" activePageId="DAG.1" focus="true">
                    <page id="Curve Editor.1"/>
                    <page id="DopeSheet.1"/>
                    <page id="DAG.1"/>
                </dock>
            </splitter>
            <split size="604"/>
            <splitter orientation="2">
                <split size="1127"/>
                <dock id="" activePageId="Properties.1">
                    <page id="Properties.1"/>
                </dock>
                <split size="197"/>
                <dock id="" activePageId="Progress.1">
                    <page id="Progress.1"/>
                    <page id="Pixel Analyzer.1"/>
                </dock>
            </splitter>
        </splitter>
    </window>
    <window x="2560" y="-8" w="2560" h="1417" maximized="1" screen="1">
        <splitter orientation="2">
            <split size="1417"/>
            <dock id="" activePageId="Viewer.1">
                <page id="Viewer.1"/>
            </dock>
        </splitter>
    </window>
</layout>
}"""
        
    root_start= f"""Root {{
 inputs 0
 name {seq_name}_{shot_name}_comp_v001.nk
 fps {fps:.2f}
 format "{width} {height} 0 0 {width} {height} 1 {resolution_label}"
"""
    if use_proxy:
        proxy_lines= """ proxy_format "4000 4000 0 0 4000 4000 1 4K Proxy LL180 Sphere"
 proxySetting always"""
    else:
        proxy_lines= """ proxy_type scale
 proxy_format "1024 778 0 0 1024 778 1 1K_Super_35(full-ap)" """
        
    if use_aces:
        color_lines= """ colorManagement OCIO
 OCIO_config aces_1.2
 defaultViewerLUT "OCIO LUTs"
 workingSpaceLUT scene_linear
 monitorLut "OCIO LUTs"
 monitorOutLUT "OCIO LUTs"
 int8Lut matte_paint
 int16Lut texture_paint
 logLut compositing_log
 floatLut scene_linear"""
    else:
        color_lines= """ colorManagement Nuke
 workingSpaceLUT linear
 monitorLut sRGB
 monitorOutLUT rec709
 int8Lut sRGB
 int16Lut sRGB
 logLut Cineon
 floatLut linear"""
        
    root_block= f"{root_start}{proxy_lines}\n{color_lines}\n}}\n"
        
    viewer_block= f"""Viewer {{
 inputs 0
 frame 1
 frame_range 1-100
 fps {fps:.8f}
 name Viewer1
 xpos -40
 ypos -9
}}"""
        
    script_text= f"""#! C:/Program Files/Nuke15.1v5/nuke-15.1.5.dll -nx
version 15.1 v5
{define_window_layout}
{root_block}
{viewer_block}
"""
    return script_text
