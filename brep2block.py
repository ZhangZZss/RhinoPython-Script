#coding=utf-8
"""
将多重曲面转化为图块，方便导出.skp
writed by Zzz
2015-01-29
"""


import Rhino as r
import scriptcontext as sc
import System as s

def main():
    #属性--设置图层
    gs = r.Input.Custom.GetString()
    gs.AcceptNothing(True)
    gs.SetCommandPrompt("请输入图块的图层名")
    while(1):
        gs.Get()
        LayerNm = gs.StringResult()
        LayerInd = sc.doc.Layers.Add(LayerNm,s.Drawing.Color.Blue)
        if(LayerInd == -1):
            if(LayerNm == ''):
                s.Windows.Forms.MessageBox.Show("未输入任何字符，程序终止")
                return
            gs.SetCommandPrompt("文件中已于相同的图层名，请重新输入")
        else:
            arr = r.DocObjects.ObjectAttributes()
            arr.LayerIndex = LayerInd
            break

    
    #选取多重曲面
    go = r.Input.Custom.GetObject()
    go.SetCommandPrompt("选择将要转换为图块的多重曲面")
    go.GeometryFilter = r.DocObjects.ObjectType.Brep
    go.GetMultiple(1,0)
    ObjRefs = go.Objects()
    
    #生成图块
    if(ObjRefs):
        point = r.Geometry.Point3d(0,0,0)
        xform = r.Geometry.Transform.Scale(point,1)
        for i,obj in enumerate(ObjRefs):
            name = '图块%2s' %i
            brep = obj.Brep()
            idef = sc.doc.InstanceDefinitions.Find(name,True)
            if(idef):
                sc.doc.InstanceDefinitions.Delete(idef.Index,True,True)
            index = sc.doc.InstanceDefinitions.Add(name,"",point,brep,arr)
            print sc.doc.Objects.AddInstanceObject(index,xform,arr)
    
    s.Windows.Forms.MessageBox.Show("共生成了%d个图块" % (i+1))
    
main()