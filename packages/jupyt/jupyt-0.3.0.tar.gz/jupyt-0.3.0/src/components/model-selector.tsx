import React, { useState, useEffect } from 'react';
import {
  Box,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  SelectChangeEvent,
  Typography,
  CircularProgress
} from '@mui/material';
import { AuthService } from '../services/auth-service';
import { getApiKey, getModelConfig, saveModelConfig } from '../config';
import { IModelConfig } from '../types/api';

interface IModelSelectorProps {
  onChange?: (config: IModelConfig) => void;
}

export function ModelSelector({ onChange }: IModelSelectorProps): JSX.Element {
  const [availableModels, setAvailableModels] = useState<{
    [provider: string]: string[];
  }>({});
  const [allModels, setAllModels] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [modelConfig, setModelConfig] =
    useState<IModelConfig>(getModelConfig());

  useEffect(() => {
    const fetchModels = async () => {
      setLoading(true);
      setError(null);

      try {
        const apiKey = getApiKey();
        if (!apiKey) {
          setError('API key not found. Please log in.');
          setLoading(false);
          return;
        }

        const authService = AuthService.getInstance();
        const response = await authService.getAvailableModels(apiKey);
        setAvailableModels(response.available_models);

        // Combine all models from different providers into a single array
        const combinedModels: string[] = [];
        Object.entries(response.available_models).forEach(
          ([provider, models]) => {
            models.forEach(model => {
              combinedModels.push(model);
            });
          }
        );
        setAllModels(combinedModels);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch models');
      } finally {
        setLoading(false);
      }
    };

    fetchModels();
  }, []);

  const handleModelChange = (event: SelectChangeEvent) => {
    const selectedModel = event.target.value;

    // Find which provider this model belongs to
    let selectedProvider = '';
    Object.entries(availableModels).forEach(([provider, models]) => {
      if (models.includes(selectedModel)) {
        selectedProvider = provider;
      }
    });

    const newConfig = {
      ...modelConfig,
      provider: selectedProvider,
      model: selectedModel
    };

    console.log('Selected model:', selectedModel);
    setModelConfig(newConfig);
    saveModelConfig(newConfig);
    onChange?.(newConfig);
  };

  if (loading) {
    return (
      <Box
        sx={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          p: 2
        }}
      >
        <CircularProgress size={24} sx={{ mr: 1 }} />
        <Typography variant="body2">Loading models...</Typography>
      </Box>
    );
  }

  if (error) {
    return (
      <Box sx={{ p: 2 }}>
        <Typography variant="body2" color="error">
          {error}
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ display: 'flex', flexDirection: 'row', gap: 2, p: 2 }}>
      <FormControl fullWidth size="small">
        <InputLabel id="model-select-label">Model</InputLabel>
        <Select
          labelId="model-select-label"
          id="model-select"
          value={modelConfig.model}
          label="Model"
          onChange={handleModelChange}
        >
          {allModels.map(model => (
            <MenuItem key={model} value={model}>
              {model}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    </Box>
  );
}
