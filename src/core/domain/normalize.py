def normalize_byte (value :int )->float :
    if not 0 <=value <=255 :
        raise ValueError (f"value deve estar entre 0 e 255, recebido: {value}")
    return value /255.0 

def normalize_word (value :int )->float :
    if not 0 <=value <=65535 :
        raise ValueError (f"value deve estar entre 0 e 65535, recebido: {value}")
    return value /65535.0 

def denormalize_byte (value :float )->int :
    if not 0.0 <=value <=1.0 :
        raise ValueError (f"value deve estar entre 0.0 e 1.0, recebido: {value}")
    return round (value *255.0 )

def denormalize_word (value :float )->int :
    if not 0.0 <=value <=1.0 :
        raise ValueError (f"value deve estar entre 0.0 e 1.0, recebido: {value}")
    return round (value *65535.0 )

def clamp (value :float ,min_val :float ,max_val :float )->float :
    if min_val >max_val :
        raise ValueError (f"min_val deve ser menor ou igual a max_val, recebido: min={min_val}, max={max_val}")
    return max (min_val ,min (max_val ,value ))
