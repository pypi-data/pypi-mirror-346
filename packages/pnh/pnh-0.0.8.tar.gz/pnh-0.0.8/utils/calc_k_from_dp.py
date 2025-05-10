import pandapipes 
import networkx as nx
import math
import logging
import sys

logger = logging.getLogger('pnh.utils.calc_k_from_dp')

try:
    import pnh.utils.gen_model_from_nx as gen_model_from_nx 
except Exception as e:
    logger.debug(f"ImportError: 'import pnh.utils.gen_model_from_nx as gen_model_from_nx' - trying 'import gen_model_from_nx' instead ... maybe pip install -e . is active ...")                 
    import utils.gen_model_from_nx as gen_model_from_nx 


def pp(
        nxg=nx.Graph()
       ,ppn=pandapipes.pandapipesNet

       # pipe data keys in
       ,dpFL_SP='dpFL_SP' 

       # pipe data keys out
       ,k_MV='k_MV' 

       # min. allowed k in [mm]
       ,k_min=0.001
):
    """ Calculates roughnesses according to pipe-wise given pressure friction losses.
    
    :param nxg: networkx graph with pnh-data
    :param ppn: pandapipes net generated from nxg above (via pnh.utils.gen_model_from_nx.pp) and already calculated

    :param dpFL_SP: i.e. 'dpFL_SP'; pipe data key: pipe friction loss due to colebrook-friction in [bar] (setpoint)
    :param k_MV: i.e. 'k_MV'; pipe data key: calculated roughness (manipulated variable)
    :param k_min: min. allowed k in [mm]

    """

    logStr=f"{sys._getframe().f_code.co_name}:"
    logger.debug(f"{logStr} Start.") 

    dfPipes=ppn.pipe.merge(ppn.res_pipe,left_index=True,right_index=True)
    dfJunctions=ppn.junction.merge(ppn.res_junction,left_index=True,right_index=True)

    # over all pipes
    for u, v, data in nxg.edges(data=True):
        
        # 2-node, 1-pipe subgraph
        nxg1Pipe = nxg.subgraph([u,v])

        suNode=dfJunctions.loc[nxg1Pipe.nodes[u][gen_model_from_nx.idKey],:]
        svNode=dfJunctions.loc[nxg1Pipe.nodes[v][gen_model_from_nx.idKey],:]
        s1Pipe=dfPipes.loc[nxg1Pipe.edges[u,v][gen_model_from_nx.idKey],:]

        #logger.debug(f"{logStr} suNode: {suNode.to_string()}") 
        #logger.debug(f"{logStr} svNode: {svNode.to_string()}") 
        #logger.debug(f"{logStr} s1Pipe: {s1Pipe.to_string()}") 

        # create model
        ppn1Pipe = pandapipes.create_empty_network(fluid=pandapipes.get_fluid(ppn))

        u1=pandapipes.create_junction(ppn1Pipe
                            ,pn_bar=suNode.pn_bar
                            ,tfluid_k=suNode.tfluid_k
                            ,height_m=suNode.height_m
                            ,nameStr=suNode.nameStr
        )
        v1=pandapipes.create_junction(ppn1Pipe
                            ,pn_bar=svNode.pn_bar
                            ,tfluid_k=svNode.tfluid_k
                            ,height_m=svNode.height_m
                            ,nameStr=svNode.nameStr
        )        
    
        if gen_model_from_nx.alphaKey in data.keys() and gen_model_from_nx.TaKey in data.keys():
                    logger.debug(f"{logStr} heat transfer data available") 
                    heat_transfer_data=True
                    pandapipes.create_pipe_from_parameters(ppn1Pipe
                                                    ,from_junction=u1
                                                    ,to_junction=v1
                                                    ,length_km=s1Pipe.length_km
                                                    ,diameter_m=s1Pipe.diameter_m
                                                    ,k_mm=s1Pipe.k_mm
                                                    ,nameStr=s1Pipe.nameStr
                                                    #
                                                    ,alpha_w_per_m2k=s1Pipe.alpha_w_per_m2k
                                                    ,text_k=s1Pipe.text_k
                    )            
        else:
                    heat_transfer_data=False
                    pandapipes.create_pipe_from_parameters(ppn1Pipe
                                                    ,from_junction=u1
                                                    ,to_junction=v1
                                                    ,length_km=s1Pipe.length_km
                                                    ,diameter_m=s1Pipe.diameter_m
                                                    ,k_mm=s1Pipe.k_mm
                                                    ,nameStr=s1Pipe.nameStr
                    )

        # create Bcs
        if s1Pipe.mdot_from_kg_per_s > 0.:
            # sink in v
            pandapipes.create_sink(ppn1Pipe  
                                ,junction=v1
                                ,mdot_kg_per_s=s1Pipe.mdot_from_kg_per_s
            )
            # p in u
            if heat_transfer_data:
                pandapipes.create_ext_grid(ppn1Pipe
                                    ,junction=u1
                                    ,p_bar=s1Pipe.p_from_bar
                                    ,t_k=s1Pipe.t_from_k
                )      
                logger.debug(f"{logStr} pT-Q (sink)")                  
            else:
                pandapipes.create_ext_grid(ppn1Pipe
                                    ,junction=u1
                                    ,p_bar=s1Pipe.p_from_bar
                )
                logger.debug(f"{logStr} p-Q (sink)") 
        elif s1Pipe.mdot_from_kg_per_s < 0.:
            # sink in u
            pandapipes.create_sink(ppn1Pipe  
                                ,junction=u1
                                ,mdot_kg_per_s=-s1Pipe.mdot_from_kg_per_s
            )       
            # p in v
            if heat_transfer_data:
                pandapipes.create_ext_grid(ppn1Pipe
                                    ,junction=v1
                                    ,p_bar=s1Pipe.p_to_bar
                                    ,t_k=s1Pipe.t_to_k
                )       
                logger.debug(f"{logStr} (sink) Q-pT")                              
            else:
                pandapipes.create_ext_grid(ppn1Pipe
                                    ,junction=v1
                                    ,p_bar=s1Pipe.p_to_bar
                )   
                logger.debug(f"{logStr} (sink) Q-p")                 
        else:            
            logger.info(f"{logStr} No Flow?!") 
            continue
            
        # calculate
        if heat_transfer_data:
            pandapipes.pipeflow(ppn1Pipe
                ,friction_model='colebrook'     
                ,mode='bidirectional'   
            )             
        else:
            pandapipes.pipeflow(ppn1Pipe
                ,friction_model='colebrook'        
            )

        # examine the result
        s1Pipe_ppn1Pipe=ppn1Pipe.pipe.merge(ppn1Pipe.res_pipe,left_index=True,right_index=True).iloc[0]

        resultIdentical=s1Pipe_ppn1Pipe.equals(s1Pipe)

        if not resultIdentical:
              logger.warning(f"{logStr} Initial 1Pipe calculation differs?!")
              logger.debug(f"{logStr} s1Pipe: {s1Pipe.to_string()}") 
              logger.debug(f"{logStr} s1Pipe_ppn1Pipe: {s1Pipe_ppn1Pipe.to_string()}") 
              
        k=pp_calc_roughness(
          ppn1Pipe=ppn1Pipe
         ,dpFL_SP=data[dpFL_SP]
         ,k_min=k_min
        )
        logger.debug(f"{logStr} k: {k:.4f}") 
        nxg.edges[u,v].update({k_MV:k})

    logger.debug(f"{logStr} End.") 

def pp_calc_roughness(
          ppn1Pipe=pandapipes.pandapipesNet
         ,dpFL_SP=4.
         ,dpFL_ER=0.001
         ,dk=1
         ,k_min=0.001
         ,depth=0
):
    """ Calculates roughness according to given pressure friction loss.
    
    :param ppn1Pipe: pandapipes 2Node, 1Pipe net already calculated
    :param dpFL_SP: pipe friction loss in flow direction due to colebrook-friction in [bar] (setpoint)
    :param dpFL_ER: max. allowed pipe friction loss deviation in abs. [bar]
    :param k_min: min. allowed k in [mm]

    :return: calculated k in [mm]

    Note: Returns existing k if no flow or existing k <= k_min.

    """

    logStr=f"{sys._getframe().f_code.co_name}:"
    logger.debug(f"{logStr} Start. depth: {depth}") 

    dfPipe=ppn1Pipe.pipe.merge(ppn1Pipe.res_pipe,left_index=True,right_index=True)
    dfPipe=dfPipe.merge(ppn1Pipe.junction,left_on='from_junction',right_index=True).filter(items=dfPipe.columns.to_list()+['height_m'],axis=1).rename(columns={'height_m':'height_from_m'})
    dfPipe=dfPipe.merge(ppn1Pipe.junction,left_on='to_junction',right_index=True).filter(items=dfPipe.columns.to_list()+['height_m'],axis=1).rename(columns={'height_m':'height_to_m'})
    s1Pipe=dfPipe.iloc[0]

    if s1Pipe.mdot_from_kg_per_s == 0.:
        logger.debug(f"{logStr} No Flow?!") 
        logger.debug(f"{logStr} Done.") 
        return s1Pipe.k_mm
        
    # calculate dps
    dp,dpFL_PV,dp_DZ=pp_calc_dp(s1Pipe,ppn1Pipe['fluid'])

    logger.debug(f"{logStr}                 pFrom: {s1Pipe.p_from_bar:7.4f}     pTo: {s1Pipe.p_to_bar:7.4f}") 
    logger.debug(f"{logStr} in flow direction: dp: {dp:7.4f}    dpFL: {dpFL_PV:7.4f} dpDZ: {dp_DZ:7.4f}") 

    if 'alpha_w_per_m2k' in ppn1Pipe.pipe.columns.to_list():
         heat_transfer_data=True
    else:
         heat_transfer_data=False

    if heat_transfer_data:
        logger.debug(f"{logStr}                TFrom: {s1Pipe.t_from_k-273.15:7.2f}     TTo: {s1Pipe.t_to_k-273.15:7.2f}") 

    # calculate deviation
    dpFL_DV=dpFL_SP-dpFL_PV

    if math.fabs(dpFL_DV) <= dpFL_ER:
  
        logger.debug(f"{logStr} Convergence: dpFL_DV: {dpFL_DV:+.4f} dpFL_ER: {dpFL_ER:+.4f} k: {s1Pipe.k_mm:.4f} (dk={dk:.4f})") 
        logger.debug(f"{logStr}              dpFL_SP: {dpFL_SP:+.4f} dpFL_PV: {dpFL_PV:+.4f}") 
        logger.debug(f"{logStr}                pFrom: {s1Pipe.p_from_bar:7.4f}     pTo: {s1Pipe.p_to_bar:7.4f}") 
        if heat_transfer_data:
            logger.debug(f"{logStr}                TFrom: {s1Pipe.t_from_k-273.15:7.2f}     TTo: {s1Pipe.t_to_k-273.15:7.2f}")         
        logger.debug(f"{logStr} Done.") 
        return s1Pipe.k_mm

    # Starting sign of the deviation
    dpFL_DVVStart=math.copysign(1,dpFL_DV)
    dpFL_DVV=dpFL_DVVStart

    # with the same k-value change dk until the sign of the deviation changes 
    while dpFL_DVV==dpFL_DVVStart and ppn1Pipe.pipe.loc[0,'k_mm']>k_min:

        # adjust roughness in the right direction
        if dpFL_DVV > 0:
            # increase roughness
            dkAdd=dk
        else:
            # reduce roughness
            dkAdd=-dk
        k_new=ppn1Pipe.pipe.loc[0,'k_mm']+dkAdd
        if k_new < k_min:
             logger.debug(f"{logStr} k_new: {k_new} < k_min: {k_min}: k_new==k_min ...")  
             # k + dk = k_min
             dk = math.fabs(k_min - ppn1Pipe.pipe.loc[0,'k_mm'])
             dkAdd=-dk
             k_new=ppn1Pipe.pipe.loc[0,'k_mm']+dkAdd
                         
        
        ppn1Pipe.pipe.loc[0,'k_mm']=k_new           

        # calculate with new roughness
        if heat_transfer_data:
            pandapipes.pipeflow(ppn1Pipe
                    ,friction_model='colebrook'        
                    ,mode='bidirectional'
                    )                          
        else:
            pandapipes.pipeflow(ppn1Pipe
                    ,friction_model='colebrook'        
                    )        
        
        dfPipe=ppn1Pipe.pipe.merge(ppn1Pipe.res_pipe,left_index=True,right_index=True)
        dfPipe=dfPipe.merge(ppn1Pipe.junction,left_on='from_junction',right_index=True).filter(items=dfPipe.columns.to_list()+['height_m'],axis=1).rename(columns={'height_m':'height_from_m'})
        dfPipe=dfPipe.merge(ppn1Pipe.junction,left_on='to_junction',right_index=True).filter(items=dfPipe.columns.to_list()+['height_m'],axis=1).rename(columns={'height_m':'height_to_m'})    
        s1Pipe=dfPipe.iloc[0]

        # calculate dps
        dp,dpFL_PV,dp_DZ=pp_calc_dp(s1Pipe,ppn1Pipe['fluid'])

        # calculate deviation      
        dpFL_DV=dpFL_SP-dpFL_PV

        logger.debug(f"{logStr} Iteration:   dpFL_DV: {dpFL_DV:+.4f} dpFL_ER: {dpFL_ER:+.4f} k: {s1Pipe.k_mm:.4f} (dkAdd={dkAdd:+.4f})")       
        dpFL_DVV=math.copysign(1,dpFL_DV)
    
    if dpFL_DVV!=dpFL_DVVStart and ppn1Pipe.pipe.loc[0,'k_mm']>k_min:
        # the sign of the deviation changed above k _min; continue with k-value change dk/2 ...
        k=pp_calc_roughness(ppn1Pipe=ppn1Pipe
            ,dpFL_SP=dpFL_SP
            ,dpFL_ER=dpFL_ER
            ,dk=dk/2
            ,depth=depth+1
        )
    elif dpFL_DVV!=dpFL_DVVStart and ppn1Pipe.pipe.loc[0,'k_mm']<=k_min:
        logger.debug(f"{logStr} the sign of the deviation changed @k_min; continue with k-value change dk/2 ...")       
        k=pp_calc_roughness(ppn1Pipe=ppn1Pipe
            ,dpFL_SP=dpFL_SP
            ,dpFL_ER=dpFL_ER
            ,dk=dk/2
            ,depth=depth+1
        )
    else:
         logger.debug(f"{logStr} the sign of the deviation changed not; k<=k_min; stay with k_min ...")  
         k=ppn1Pipe.pipe.loc[0,'k_mm']
         
    return k

def pp_calc_dp(
          s1Pipe
         ,fluid
):
    """ Calculates dps in flow direction.
    
    :param s1Pipe: series derived from pandapipes dfs with all data needed except:
    :param fluid: pandapipes fluid

    :return: dp,dp_FL,dp_DZ

    """

    logStr=f"{sys._getframe().f_code.co_name}:"
    logger.debug(f"{logStr} Start.") 

    if s1Pipe.mdot_from_kg_per_s > 0.:
        dp=s1Pipe.p_from_bar-s1Pipe.p_to_bar
        dz=s1Pipe.height_from_m-s1Pipe.height_to_m
    elif s1Pipe.mdot_from_kg_per_s < 0.:
        dp=s1Pipe.p_to_bar-s1Pipe.p_from_bar
        dz=s1Pipe.height_to_m-s1Pipe.height_from_m
    else:
        logger.error(f"{logStr} No Flow?!") 
        logger.debug(f"{logStr} Done.") 
        dp_FL=0

    rho_from=fluid.get_density(temperature=s1Pipe.t_from_k) 
    rho_to=fluid.get_density(temperature=s1Pipe.t_to_k) 
    dp_DZ=dz*.5*(rho_from+rho_to)*9.81*1.e-5
    dp_FL=dp+dp_DZ

    logger.debug(f"{logStr} End.") 
    return dp,dp_FL,dp_DZ