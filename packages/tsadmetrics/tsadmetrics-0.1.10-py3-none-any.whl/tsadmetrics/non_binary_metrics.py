import numpy as np
from ._tsadeval.metrics import *
from .metric_utils import transform_to_full_series
from sklearn.metrics import auc
from .binary_metrics import point_adjusted_precision, point_adjusted_recall, segment_wise_precision, segment_wise_recall
from pate.PATE_metric import PATE
def precision_at_k(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = PatK_pw(y_true,y_anomaly_scores)

    return m.get_score()

def auc_roc_pw(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = AUC_ROC(y_true,y_anomaly_scores)

    return m.get_score()


def auc_pr_pw(y_true : np.array ,y_anomaly_scores:  np.array):
    
    m = AUC_PR_pw(y_true,y_anomaly_scores)

    return m.get_score()



def auc_pr_pa(y_true: np.array, y_anomaly_scores: np.array):
    precisions = [1]
    recalls = [0]
    tps,fps,fns = [],[],[]

    p_adj = PointAdjust(len(y_true),y_true,(np.array(y_anomaly_scores) >= 0.5).astype(int))
    segments= p_adj.get_gt_anomalies_segmentwise()
    idx = np.argsort(y_anomaly_scores)[::-1].astype(int)
    y_true_sorted = np.array(y_true)[idx]
    y_anomaly_scores_sorted = np.array(y_anomaly_scores)[idx]
    
    segment_mins = []
    for start,end in segments:
        anoms_scores = y_anomaly_scores[start:end+1]
        segment_mins.append([np.max(anoms_scores),end-start+1])

    for i_t in range(len(y_anomaly_scores_sorted)):
        fp,tp,fn = 0,0,0
        if i_t > 0 and y_anomaly_scores_sorted[i_t] == y_anomaly_scores_sorted[i_t-1] :
            tp = tps[-1]
            fp = fps[-1]
            fn = fns[-1]
        else:
            if y_true_sorted[i_t] == 0:
                #FP
                if len(fps)==0:
                    aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int)
                    for i in range(len(aux_y_pred)):
                        if aux_y_pred[i] == 1 and y_true[i] == 0:
                            fp+=1


                else:
                    fp=fps[i_t-1]+1
            else:
                if len(fps)==0:
                    aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int)
                    for i in range(len(aux_y_pred)):
                        if aux_y_pred[i] == 1 and y_true[i] == 0:
                            fp+=1
                else:
                    fp=fps[i_t-1]
            for score, length in segment_mins:
                if score >= y_anomaly_scores_sorted[i_t]:
                    #TP
                    tp+= length
                else:
                    #FN
                    fn+= length
        tps.append(tp)
        fns.append(fn)
        fps.append(fp)
    for tp,fp,fn in zip(tps,fps,fns):
        if tp>0:
            precisions.append(tp/(tp+fp))
            recalls.append(tp/(tp+fn))
        else:
            precisions.append(0)
            recalls.append(0)    
      
    
    recalls.append(1)
    precisions.append(0)

    auc_value = auc(recalls, precisions)
    return auc_value




def auc_pr_sw(y_true: np.array, y_anomaly_scores: np.array):
    precisions = [1]
    recalls = [0]
    tps,fps,fns = [],[],[]


    segments = []
    i=0
    while i < len(y_true):
        if y_true[i] == 1:
            start = i
            end = i
            while i < len(y_true) and y_true[i] == 1:
                end = i
                i += 1
            segments.append([start,end])
        i+=1
    idx = np.argsort(y_anomaly_scores)[::-1].astype(int)
    y_anomaly_scores_sorted = np.array(y_anomaly_scores)[idx]
    
    segment_mins = []
    for start,end in segments:
        anoms_scores = y_anomaly_scores[start:end+1]
        segment_mins.append([np.max(anoms_scores),[start,end]])

    for i_t in range(len(y_anomaly_scores_sorted)):
        fp,tp,fn = 0,0,0
        
            
        aux_y_pred = (y_anomaly_scores >= y_anomaly_scores_sorted[i_t]).astype(int) 
        for score,seg in segment_mins:
            start,end = seg
            if score >= y_anomaly_scores_sorted[i_t]:
                #TP
                tp+= 1
                if aux_y_pred[start]== 1:
                    # Extender hacia la izquierda
                    i = start - 1
                    while i >= 0 and aux_y_pred[i] == 1:
                        aux_y_pred[i] = 0
                        i -= 1
                
                if aux_y_pred[end] == 1:
                    # Extender hacia la derecha
                    i = end + 1
                    while i < len(aux_y_pred) and aux_y_pred[i] == 1:
                        aux_y_pred[i] = 0
                        i += 1
                aux_y_pred[start:end+1] = 0

            else:
                #FN
                fn+= 1
        
        if np.sum(aux_y_pred)>0:
            fpsegments = []
            i=0
            while i < len(aux_y_pred):
                if aux_y_pred[i] == 1:
                    start = i
                    end = i
                    while i < len(aux_y_pred) and aux_y_pred[i] == 1:
                        end = i
                        i += 1
                    fpsegments.append([start,end])
                i+=1
            fp = len(fpsegments)
        else:
            fp = 0
            
            
        tps.append(tp)
        fns.append(fn)
        fps.append(fp)
    for tp,fp,fn in zip(tps,fps,fns):
        if tp>0:
            precisions.append(tp/(tp+fp))
            recalls.append(tp/(tp+fn))
        else:
            precisions.append(0)
            recalls.append(0)    
      
    

    auc_value = auc(recalls, precisions)

    return auc_value


def vus_roc(y_true : np.array ,y_anomaly_scores:  np.array, window=4):
    
    m = VUS_ROC(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def vus_pr(y_true : np.array ,y_anomaly_scores:  np.array,  window=4):
    
    m = VUS_PR(y_true,y_anomaly_scores,max_window=window)

    return m.get_score()


def real_pate(y_true: np.array, y_anomaly_scores: np.array, early: int, delay: int):
    """
    Calculate PATE score for anomaly detection in time series.
    The PATE score is the ratio of the number of true positives to the sum of true positives, false positives, and false negatives, within a given early and delay range.

    Parameters:
    y_true (np.array): The ground truth binary labels for the time series data.
    y_anomaly_scores (np.array): The predicted binary labels for the time series data.
    early (int): The maximum number of time steps before an anomaly must be predicted to be considered early.
    delay (int): The maximum number of time steps after an anomaly must be predicted to be considered delayed.

    Returns:
    float: The PATE score.
    """
    
    return PATE(y_true, y_anomaly_scores, early, delay, binary_scores=False)