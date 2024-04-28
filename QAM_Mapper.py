import numpy as np

class QAM_Mapper:
    def __init__(self,num_bits_per_symbol):
        self._num_bits_per_symbol = num_bits_per_symbol
        self._bits,self._values = self.generate_qam()

    def generate_qam(self):
        num_bits = self._num_bits_per_symbol
        mod_order = np.power(2,num_bits)
        all_bits = np.array(list(np.binary_repr(i, width=num_bits) for i in range(mod_order)))
    
        qam_values = []
        for i in range(mod_order):
            real = int(all_bits[i][:num_bits//2], 2)
            imag = int(all_bits[i][num_bits//2:], 2)
            qam_values.append((2 * real - (num_bits - 1)) + 1j * (2 * imag - (num_bits - 1)))
            
        normalised = np.sqrt(np.mean(np.square(np.abs(qam_values))))
        qam_bits = [[int(bit) for bit in bits_str] for bits_str in all_bits]
        qam_values = qam_values/normalised
        return qam_bits,qam_values
    
    def qam_modulation(self,input):
        qam_signal = self._bits
        qam_values = np.array(self._values).astype(complex)
        binary_code = np.reshape(input,(len(input)//self._num_bits_per_symbol,self._num_bits_per_symbol)).astype(int)
    
        mapping = []
        for _,data in enumerate(binary_code):
            for i,data_point in enumerate(qam_signal):
                if(np.all(data == data_point)):
                    mapping.append(qam_values[i])
        mapping = np.array(mapping).astype(complex)
        return mapping
    
    def qam_demodulation(self,input):
        qam_signal = self._bits
        qam_values = np.array(self._values).astype(complex)
        mapper = np.array(input).reshape(-1)
        
        distances = np.abs(np.expand_dims(mapper, axis=1) - qam_values)
        demodulated_indices = np.argmin(distances, axis=1)
        demodulated_indices = np.array(demodulated_indices)
  
        demodulated_values = []
        for i in range(len(demodulated_indices)):
            index = demodulated_indices[i]
            demodulated_values.append(qam_signal[index])
        demodulated_values = np.array(np.squeeze(demodulated_values).reshape(-1),dtype=int)
        return demodulated_values
         