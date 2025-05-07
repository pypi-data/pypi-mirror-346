import torch
import torch.nn as nn
import torch.nn.functional as F

class SPConv2d(nn.Module):
    def __init__(self, in_channels, out_channels, kernel_size=3, 
                 stride=1, padding=0, threshold_init=0.1, scale_init=10.0):
        super().__init__()
        assert kernel_size == 3, "Kernel size must be 3x3"
        self.stride = stride
        self.padding = padding
        
        # Device-agnostic parameter initialization
        self.core = nn.Parameter(torch.empty(out_channels, in_channels, 1, 1))
        self.threshold = nn.Parameter(torch.tensor([threshold_init]))
        self.scale = nn.Parameter(torch.tensor([scale_init]))
        self.periphery = nn.Parameter(torch.empty(8))
        
        nn.init.kaiming_uniform_(self.core)
        nn.init.uniform_(self.periphery, -0.1, 0.1)

    def forward(self, x):
        # Automatically use same device as input
        core = self.core.to(x.device)
        periphery = self.periphery.to(x.device)
        threshold = self.threshold.to(x.device)
        scale = self.scale.to(x.device)
        
        B, C, H, W = x.shape
        patches = F.unfold(x, kernel_size=3, stride=self.stride, padding=self.padding)
        patches = patches.view(B, C, 9, -1)
        H_out = (H + 2*self.padding - 3) // self.stride + 1
        W_out = (W + 2*self.padding - 3) // self.stride + 1
        
        center = patches[:, :, 4, :].unsqueeze(2)
        diffs = (patches - center) ** 2
        div = diffs.sum(dim=(1,2)).view(B, H_out, W_out)
        
        m_soft = torch.sigmoid((div - self.threshold) * self.scale).unsqueeze(1)
        m_hard = (m_soft > 0.5).float()
        mask = m_hard.detach() - m_soft.detach() + m_soft
        
        out = torch.zeros(B, self.out_channels, H_out, W_out, device=x.device)

        zeros = torch.where(m_hard.view(B, -1) == 0)
        if zeros[0].numel():
            b_idx, pos = zeros
            cen = center.squeeze(2)                
            vals = cen[b_idx, :, pos]             
            w   = self.core.view(self.out_channels, self.in_channels)  
            out.view(B, self.out_channels, -1)[b_idx, :, pos] = vals @ w.t()

        ones = torch.where(m_hard.view(B, -1) == 1)
        if ones[0].numel():
            b_idx, pos = ones
            flat = patches.permute(0,3,1,2).reshape(-1, C, 9) 
            sel  = flat[b_idx * L + pos]                  
            peri = sel[:, :, [0,1,2,3,5,6,7,8]]         
            w    = peri * self.periphery.view(1,1,8)     
            agg  = w.sum(dim=2)                           
            w1   = self.core.view(self.out_channels, self.in_channels)
            out.view(B, self.out_channels, -1)[b_idx, :, pos] = agg @ w1.t()

        return out