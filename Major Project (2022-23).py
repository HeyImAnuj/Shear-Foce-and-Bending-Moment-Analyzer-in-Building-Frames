import numpy as np
import matplotlib.patches as patches
import matplotlib.pyplot as plt

print("************************************************************")
print("**************** ||     MAJOR PROJECT     ||****************")
print("************************************************************")
print('By: Prachi Pardhi, Sakshi Pathak, Anuj Patel')
# =============================================================================
# Input Part
# =============================================================================

height=int(input("Please Enter the Height of each Storey : "))
storey=int(input("Please Enter the Number of Storey : "))
bay=int(input("Please Enter the Number of Bay : "))
print('')
print('---||---')

widths_bay=[]
print("please input the Widths of bay :-")
for i in range(bay):
    print('Bay ',i+1,end=' ')
    a=float(input("Width = "))
    widths_bay.append(a)
    
print('')
print('---||---')
force=[]
print("please input the Forces on Storey :-")
for i in range(storey):
    print('Storey ',i+1,end=' ')
    a=float(input("Force = "))
    force.append(a)





# height = 10 # Floor height
# storey = 3
# bay = 2
bay_widths = np.array(widths_bay)
#force_list = np.array([10, 8.5, 7, 5, 3.5, 2])
force_list = np.array(force)

bay_widths_cm = np.hstack((0,bay_widths.cumsum()))
heights = height*np.ones(storey)
heights_cm = np.hstack((0,heights.cumsum()))

h_line = storey*bay
v_line = (bay+1)*storey

print('')
print("--------Figure of Frame--------")
def frame():
    fig= plt.figure(figsize=(10,10))
    ax = fig.add_subplot(1,1,1)


    for i in range(storey):
        for j in range(bay):        
            ax.plot([bay_widths_cm[j],bay_widths_cm[j+1]],[heights_cm[i+1], heights_cm[i+1]], color='blue') #Horizontal line

    for i in range(storey):
        for j in range(bay+1):
            ax.plot([bay_widths_cm[j], bay_widths_cm[j]], [heights_cm[i], heights_cm[i+1]], color='blue')
    return fig, ax


fig, ax = frame()
for i in range(storey):
    arl = 5
    ax.annotate(str(force_list[i]), xytext=[-arl, heights_cm[i+1]-0.7],
                 xy=[0, heights_cm[i+1]], 
                 arrowprops=dict(arrowstyle="->", color='red'),
                fontsize=12, size=20)
ax.set_xlim(-bay_widths[0]*0.3, np.max(bay_widths_cm) + bay_widths[0]*0.3)
fig.savefig('Frame_with_lateral_load.png', dpi=300)

shear_unit = force_list[::-1].cumsum()/(bay*2)
csf = np.zeros((storey, bay+1))
csf_shape=np.shape(csf) #shear force for column
cmt = np.zeros((storey, bay+1))#Bending moment for column
bmt = np.zeros((storey, bay))#Bending moment for beam
for i in range(storey):
    csf[i]=shear_unit[i]*2
    csf[i, 0] = shear_unit[i]
    csf[i, -1] = shear_unit[i]

## Shear force diagram for column
print('')
print('---- Shear force diagram for column ----')
fig_f, ax_f = frame()
for i in range(storey):
    for j in range(bay+1):
        ax_f.text(bay_widths_cm[j], heights_cm[i]+(height/2) , csf[::-1][i,j])
        rect = patches.Rectangle((bay_widths_cm[j],heights_cm[i]),
                                 csf[::-1][i,j]*0.4,height,linewidth=1,edgecolor='r',facecolor='green', alpha=0.5)
        ax_f.add_patch(rect)
        #ax_f.text(bay_widths_cm[j]-2, heights_cm[i]+1 , csf[::-1][i,j]*height*0.5)
        #ax_f.text(bay_widths_cm[j]-2, heights_cm[i]+height-1.5 , csf[::-1][i,j]*height*0.5)
ax_f.set_xlim(-bay_widths[0]*0.3, np.max(bay_widths_cm) + bay_widths[0]*0.3)
fig_f.savefig('Shear_force_column.png', dpi=300)


## Bending moment diagram for column
print('')
print('---- Bending moment diagram for column ----')
fig_g, ax_g = frame()
for i in range(storey):
    for j in range(bay+1):
        mnt = csf[::-1][i,j] * height/2
        cmt[i,j]=mnt
        ax_g.text(bay_widths_cm[j], heights_cm[i]+(height/2) , mnt)
        #rect = patches.Rectangle((bay_widths_cm[j],heights_cm[i]),
        #                         csf[::-1][i,j]*0.4,height,linewidth=1,edgecolor='r',facecolor='none')
        ax_g.plot([bay_widths_cm[j], bay_widths_cm[j]+(mnt*0.05),  bay_widths_cm[j]-(mnt*0.05), bay_widths_cm[j]],
                  [heights_cm[i], heights_cm[i], heights_cm[i]+height, heights_cm[i]+height], 
                          color='red')
        #ax_f.add_patch(rect)

ax_g.set_xlim(-bay_widths[0]*0.3, np.max(bay_widths_cm) + bay_widths[0]*0.3)
fig_g.savefig('Moment_diagram_column.png', dpi=300)

## Bending moment diagram for Beam
print('')
print('---- Bending moment diagram for Beam ----')
fig_h, ax_h = frame()
for i in range(storey):
    for j in range(bay):
        bmb = (cmt[i,0]+cmt[i+1,0]) if i+1<=storey-1 else cmt[i,0]
        bmt[i,j]=bmb
        ax_h.text((bay_widths_cm[j]+bay_widths_cm[j+1])/2, heights_cm[i+1] , bmb)
        ax_h.plot([bay_widths_cm[j], bay_widths_cm[j], bay_widths_cm[j+1], bay_widths_cm[j+1]],
                  [heights_cm[i+1], heights_cm[i+1]+(bmb*0.04), heights_cm[i+1]-(bmb*0.04), heights_cm[i+1]], color='red')
        #print ('Storey:',i,'Bay:',j,'Column_shear:',bmb)
        #ax_g.text(bay_widths_cm[j], heights_cm[i]+(height/2) , mnt)


ax_h.set_xlim(-bay_widths[0]*0.3, np.max(bay_widths_cm) + bay_widths[0]*0.3)
fig_h.savefig('Moment_diagram_beam.png', dpi=300)

## Shear force diagram beam

fig_i, ax_i = frame()
for i in range(storey):
    for j in range(bay):
        sf = np.round(bmt[i,j]/(bay_widths[j]*0.5),2) #Shear force
        ax_i.text((bay_widths_cm[j]+bay_widths_cm[j+1])/2, heights_cm[i+1] , sf)
        #ax_i.plot([bay_widths_cm[j], bay_widths_cm[j], bay_widths_cm[j+1], bay_widths_cm[j+1]],
        #          [heights_cm[i+1], heights_cm[i+1]+(sf*0.4), heights_cm[i+1]+(sf*0.4), heights_cm[i+1]], color='red')
        
        
        rect = patches.Rectangle((bay_widths_cm[j],heights_cm[i+1]),
                         bay_widths[j],sf*0.4,linewidth=1,edgecolor='r',facecolor='green', alpha=0.5)
        ax_i.add_patch(rect)
        
print('')
print('---- Shear Force diagram for Beam ----')
ax_i.set_xlim(-bay_widths[0]*0.3, np.max(bay_widths_cm) + bay_widths[0]*0.3)
fig_i.savefig('Shear_diagram_beam.png', dpi=300)