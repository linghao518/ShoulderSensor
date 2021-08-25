from __future__ import print_function, division
from torchinfo import summary
import torch.nn.functional as F
import torch
import torch.nn as nn


class LSTM(nn.Module):

    def __init__(self, batch_size, inp_dim, mid_dim, num_layers, out_dim, seq_len):
        super(LSTM, self).__init__()
        self.liner_hidden_1 = 512
        self.liner_hidden_2 = 256
        self.liner_hidden_3 = 128
        self.liner_hidden_4 = 64
        self.device = torch.device(
            'cuda' if torch.cuda.is_available() else 'cpu')
        self.batch_size = batch_size
        self.inp_dim = inp_dim
        self.mid_dim = mid_dim
        self.num_layers = num_layers
        self.out_dim = out_dim
        self.seq_len = seq_len

        self.rnn = nn.LSTM(inp_dim, mid_dim, num_layers,
                           batch_first=True).to(self.device)
        # inp_dim 是LSTM输入张量的维度，我们已经根据我们的数据确定了这个值是3
        # mid_dim 是LSTM三个门 (gate) 的网络宽度，也是LSTM输出张量的维度
        # num_layers 是使用两个LSTM对数据进行预测，然后将他们的输出堆叠起来。
        self.reg = nn.Sequential(
            nn.Linear(mid_dim * seq_len, self.liner_hidden_1),
            nn.ReLU(),
            nn.Linear(self.liner_hidden_1, self.liner_hidden_2),
            nn.ReLU(),
            nn.Linear(self.liner_hidden_2, self.liner_hidden_3),
            nn.ReLU(),
            nn.Linear(self.liner_hidden_3, self.liner_hidden_4),
            nn.ReLU(),
            nn.Linear(self.liner_hidden_4, out_dim),
        )  # regression

    def forward(self, x):
        h0 = torch.zeros(self.num_layers, self.batch_size, self.out_dim).to(
            self.device)  # (num_layers,batch,output_size)
        c0 = torch.zeros(self.num_layers, self.batch_size, self.out_dim).to(
            self.device)  # (num_layers,batch,output_size)
        output, (hn, cn) = self.rnn(x, (h0, c0))
        output = output.contiguous().view(self.batch_size, -1)
        output = self.reg(output)

        return output


class Attention(nn.Module):
    def __init__(self, d_model, seq_len, dropout):
        super().__init__()
        # Project the dimension of features from that of input into d_model.
        self.prenet = nn.Linear(5, d_model)
        # TODO:
        #   Change Transformer to Conformer.
        #   https://arxiv.org/abs/2005.08100
        self.encoder_layer = nn.TransformerEncoderLayer(
            d_model=d_model, dim_feedforward=256, nhead=2
        )
        self.pred_layer = nn.Sequential(
            nn.Linear(d_model, d_model),
            nn.ReLU(),
            nn.Linear(d_model, 6),
        )

    def forward(self, mels):
        """
        args:
          mels: (batch size, length, 40)
        return:
          out: (batch size, n_spks)
        """
        # out: (batch size, length, d_model)
        out = self.prenet(mels)
        # out: (length, batch size, d_model)
        out = out.permute(1, 0, 2)
        # The encoder layer expect features in the shape of (length, batch size, d_model).
        out = self.encoder_layer(out)
        # out: (batch size, length, d_model)
        out = out.transpose(0, 1)
        # mean pooling
        stats = out.mean(dim=1)
        # out: (batch, n_output)
        out = self.pred_layer(stats)
        return out


if __name__=='__main__':
    print(summary(Attention(d_model=80, seq_len=120, dropout=0.1), input_size=(32, 120, 5)))
