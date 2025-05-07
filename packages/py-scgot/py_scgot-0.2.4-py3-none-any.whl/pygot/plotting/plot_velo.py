import numpy as np
import matplotlib.pyplot as plt
import scvelo as scv
from pygot.tools.traj.markov import velocity_graph
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from tqdm import tqdm
import pandas as pd


def plot_different_decomposed_velo(adata, groupby, n_top_genes=20):
    from adjustText import adjust_text
    cell_types = adata.obs[groupby].unique()
    if len(adata.obs[groupby].unique()) != 2:
        print('Must groupby binary')
        return
    
    cell_type0, cell_type1 = cell_types[0], cell_types[1]
    
    fitness = np.log10(abs(adata.layers['velocity_lineages'] / adata.layers['velocity_growth'])).mean(axis=0)
    velocity_difference = adata[adata.obs[groupby] == cell_type0].layers['velocity_lineages'].mean(axis=0) - adata[adata.obs[groupby] == cell_type1].layers['velocity_lineages'].mean(axis=0)
    
    #gene_df = pd.DataFrame([velocity_difference[0], stage_fitness[0]], index=['lineage_velocity_difference', 'lineage/growth ratio'], columns=dyn_genes).T
    gene_df = pd.DataFrame([velocity_difference, fitness], 
    index=['lineage_velocity_difference', 'lineage/growth ratio'], columns=adata.var.index).T

    df = gene_df
    df['gene'] = df.index

    top_genes = df.loc[abs(df['lineage_velocity_difference']).sort_values(ascending=False).index[:n_top_genes]]

    
    plt.figure(figsize=(10, 6))


    scatter = plt.scatter(df['lineage_velocity_difference'], df['lineage/growth ratio'], c=df['lineage/growth ratio'], cmap='viridis', alpha=0.7, edgecolors='w', s=50)

    
    arrow_properties = dict(
            arrowstyle='->',  # Simple arrow with a head
            color='red',      # Arrow color
            linewidth=0.5,    # Arrow line width
            alpha=0.8,         # Arrow transparency     
            mutation_scale=5 
        )


    plt.title('Volcano Plot')
    plt.xlabel('velocity difference : {} - {}'.format(cell_type0, cell_type1))
    plt.ylabel('lineage/growth ratio')

    plt.colorbar(scatter, label='lineage_velocity_difference')

    texts = []
    for _, row in top_genes.iterrows():
        texts.append(plt.annotate(row['gene'], (row['lineage_velocity_difference'], row['lineage/growth ratio']), fontsize=8))

    adjust_text(texts, arrowprops=arrow_properties)

    plt.show()




def potential_embedding(adata,  basis='X_umap', cell_type_key=None, ax=None, ):
    if ax is None:
        fig, ax = plt.subplots(1,1, dpi=300)
    
    scv.pl.velocity_embedding_stream(adata, basis=basis.split('_')[-1], ax=ax, show=False,  title='GOT Potential', color=cell_type_key,  fontsize=15)
    xt = adata.obsm[basis]
    s = ax.scatter(xt[:,0], xt[:,1], s=2, c=adata.obs['ent'], cmap='Reds')
    plt.title('GOT Potential')
    plt.colorbar(
                s, ax=ax, pad=0.01, fraction=0.08, aspect=30, label='differentiation potential'
            )



def velocity_embedding_grid(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='umap', k=30, update=True, **kwargs):
    if (not 'velocity_' + basis in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, k=k)
        if 'velocity_' + basis in adata.obsm.keys():
            del adata.obsm['velocity_' + basis]
    scv.pl.velocity_embedding_grid(adata, basis=basis, **kwargs)

def velocity_embedding(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='umap', k=30, update=True, **kwargs):
    if (not 'velocity_' + basis in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, k=k)
        if 'velocity_' + basis in adata.obsm.keys():
            del adata.obsm['velocity_' + basis]
    scv.pl.velocity_embedding(adata, basis=basis, **kwargs)

def velocity_embedding_stream(adata, velocity_key='velocity_pca', embedding_key='X_pca', basis='umap', k=30, update=True, **kwargs):
    if (not 'velocity_' + basis in adata.obsm.keys()) or update:
        #project_velocity(adata, velocity_key=velocity_key, embedding_key=embedding_key, basis=basis, k=k, norm=norm)
        velocity_graph(adata, embedding_key, velocity_key, k=k)
        if 'velocity_' + basis in adata.obsm.keys():
            del adata.obsm['velocity_' + basis]
    scv.pl.velocity_embedding_stream(adata, basis=basis, **kwargs)



def velocity_embedding_3d(adata, embedding_key, velocity_key, color=None, norm=False, dimensions=[0,1,2], title='', elev=20,  azim=330, cmap = cm.viridis, ax=None, **kwargs):
    X = adata.obsm[embedding_key][:,dimensions]
    V = adata.obsm[velocity_key][:,dimensions]
    if norm:
        V = adata.obsm[velocity_key][:,dimensions] / np.linalg.norm(adata.obsm[velocity_key][:,dimensions], axis=1)[:,None]
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
    if not color is None:
        if color + '_colors' in adata.uns.keys():
            y = np.array(np.array(adata.uns[color + '_colors'])[adata.obs[color].cat.codes])
        else:
            y = adata.obs[color].to_numpy()
            norm = Normalize(vmin=y.min(), vmax=y.max())
            normalized_data = norm(y)
            y = np.array(cmap(normalized_data))
        
    if ax is None:
        fig = plt.figure(**kwargs)
        ax = fig.add_subplot(111,  projection='3d')
    ax.view_init(elev=elev,    # 仰角
             azim=azim    # 方位角
            )
    
    if color is None:
        ax.quiver(X[:, 0], X[:, 1], X[:, 2], 
                  V[:, 0], V[:, 1], V[:, 2], color='grey')
    else:
        for i in tqdm(range(V.shape[0])):
            ax.quiver(X[i, 0], X[i, 1], X[i, 2], 
                  V[i, 0], V[i,1], V[i, 2], color=y[i])
    
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.set_title(title)
    

def plot_vector(adata, embedding_key, velocity_key, color=None, dimensions=[0,1], title='', cmap = cm.viridis, **kwargs):
    X = adata.obsm[embedding_key]
    V = adata.obsm[velocity_key]
    if isinstance(cmap, str):
        cmap = plt.get_cmap(cmap)
        
    if color + '_colors' in adata.uns.keys():
        y = np.array(np.array(adata.uns[color + '_colors'])[adata.obs[color].cat.codes])
    else:
        y = adata.obs[color].to_numpy()
        norm = Normalize(vmin=y.min(), vmax=y.max())
        normalized_data = norm(y)
        y = np.array(cmap(normalized_data))
        
    
    fig = plt.figure(**kwargs)
    ax = fig.add_subplot(111)
    '''
    for i in tqdm(range(V.shape[0])):
        if color is None:
            ax.quiver(X[i, dimensions[0]], X[i, dimensions[1]],
                  V[i, dimensions[0]], V[i, dimensions[1]],  color='grey')    
        else:
            ax.quiver(X[i, dimensions[0]], X[i, dimensions[1]], 
                  V[i, dimensions[0]], V[i, dimensions[1]], color=y[i])
    '''
    ax.quiver(X[:, dimensions[0]], X[:, dimensions[1]], 
                  V[:, dimensions[0]], V[:, dimensions[1]], color=y)

    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.title(title)
    plt.show()
'''
def get_velocity_embedding(adata, model = None, idx=None, embedding_key='X_pca', basis='X_umap', k=30, time_vary=True, time_key=None, norm=False, vt = None):
    if (vt is None) and (model is not None):
        vt = pred_velocity(adata, model, idx, embedding_key, time_vary=time_vary, time_key=time_key)
    elif vt is None:
        print('please offer model or vt')
        raise ValueError
    adata.obsm['velocity_' + embedding_key.split('_')[-1]] = vt.numpy()
    if embedding_key == basis:
        #adata.obsm['velocity_' + graph_key] = vt / torch.norm(vt, dim=-1)[:, None]
        adata.obsm['velocity_' + basis.split('_')[-1]] = vt
        return adata
    
    
    tree = KDTree(adata.obsm[embedding_key])
    dist, ind = tree.query(adata.obsm[embedding_key]+vt.numpy(), k=k)
    velocity = []
    for i in tqdm(range(adata.shape[0])):
        expectation = dist[i,:] / np.sum(dist[i,:])
        expectation = 1-expectation
        v = np.sum((adata.obsm[basis][ind[i,:],:] - adata.obsm[basis][i]) * (expectation[:, None]), axis=0)
        velocity.append(v)
    
    velocity = np.array(velocity)
    if norm:
        velocity /= np.linalg.norm(velocity, axis=-1)[:, None]    
    adata.obsm['velocity_' + basis.split('_')[-1]] = velocity
'''
