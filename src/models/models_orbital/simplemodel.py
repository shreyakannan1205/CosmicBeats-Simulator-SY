"""
// Copyright (c) Microsoft Corporation.
// Licensed under the MIT license.

Created by: Om Chabra
Created on: 27 Oct 2022

@desc
    This module implements the orbital propagation model for the satellite.  
"""
import numpy as np
from datetime import datetime, timedelta

from src.models.imodel import IModel, EModelTag
from src.nodes.inode import INode
from src.simlogging.ilogger import ELogType, ILogger
from skyfield.api import load, wgs84, EarthSatellite
from skyfield.framelib import itrs
from skyfield.positionlib import build_position, Barycentric
from src.utils import Location, Time

class simplemodel(IModel):
    '''
    This model class basically calculates the orbital propagation of the satellite based on the TLE.
    It takes the timestamp of the node and updates the location of the node, i.e., satellite
    '''
    __modeltag = EModelTag.COMPUTE
    __ownernode: INode
    __supportednodeclasses = ['SatelliteBasic'] #List of node classes that this model supports
    __dependencies = []
    __earthsatellite: EarthSatellite
    __logger: ILogger
    
    @property
    def iName(self) -> str:
        """
        @type 
            str
        @desc
            A string representing the name of the model class. For example, 'ModelPower' 
        """
        return self.__class__.__name__
    
    @property
    def modelTag(self) -> EModelTag:
        """
        @type
            EModelTag
        @desc
            The model tag for the implemented model
        """
        return self.__modeltag

    @property
    def ownerNode(self):
        """
        @type
            INode
        @desc
            Instance of the owner node that incorporates this model instance.
            The subclass (implementing a model) should keep a private variable holding the owner node instance. 
            This method can return that variable.
        """
        return self.__ownernode
    
    @property
    def supportedNodeClasses(self) -> 'list[str]':
        '''
        @type
            List of string
        @desc
            A model may not support all the node implementation. 
            supportedNodeClasses gives the list of names of the node implementation classes that it supports.
            For example, if a model supports only the SatBasic and SatAdvanced, the list should be ['SatBasic', 'SatAdvanced']
            If the model supports all the node implementations, just keep the list EMPTY.
        '''
        return  self.__supportednodeclasses
    
    @property
    def dependencyModelClasses(self) -> 'list[list[str]]':
        '''
        @type
            Nested list of string
        @desc
            dependencyModelClasses gives the nested list of name of the model implementations that this model has dependency on.
            For example, if a model has dependency on the ModelPower and ModelOrbitalBasic, the list should be [['ModelPower'], ['ModelOrbitalBasic']].
            Now, if the model can work with EITHER of the ModelOrbitalBasic OR ModelOrbitalAdvanced, the these two should come under one sublist looking like [['ModelPower'], ['ModelOrbitalBasic', 'ModelOrbitalAdvanced']]. 
            So each exclusively dependent model should be in a separate sublist and all the models that can work with either of the dependent models should be in the same sublist.
            If your model does not have any dependency, just keep the list EMPTY. 
        '''
        return self.__dependencies

    # API dictionary where API name is the key and handler function is the value
    __apiHandlerDictionary = {

    }
    
    def call_APIs(self, 
                _apiName: str, 
                **_kwargs):
        '''
        This method acts as an API interface of the model. 
        An API offered by the model can be invoked through this method.
        @param[in] _apiName
            Name of the API. Each model should have a list of the API names.
        @param[in]  _kwargs
            Keyworded arguments that are passed to the corresponding API handler
        @return
            The API return
        '''
        _ret = None
        try:
            _ret = self.__apiHandlerDictionary[_apiName](self, **_kwargs)
        except Exception as e:
            print(f"[ModelOrbit]: An unhandled API request has been received by {self.__ownernode.nodeID}:", e)
            
        return _ret
        
    def __init__(
            self, 
            _ownernodeins: INode, 
            _loggerins: ILogger,
            _alwaysCalculate: bool = False) -> None:
        '''
        @desc
            Constructor of the class
        @param[in]  _ownernodeins
            Instance of the owner node that incorporates this model instance
        @param[in]  _loggerins
            Logger instance 
        @param[in]  _alwaysCalculate
            Wether to automatically update the location of the node at every time step or not. Default is False
        '''
        assert _ownernodeins is not None
        assert _loggerins is not None

        self.__ownernode = _ownernodeins
        self.__logger = _loggerins

    def __str__(self) -> str:
        return "".join(["Model name: ", self.iName, ", " , "Model tag: ", self.__modeltag.__str__()])

    def Execute(self):
        """
        @desc
            This method executes the tasks that needed to be performed by the model.
            The model reads the time of the owner node which is a satellite and updates its location
        """
        pos = self.__ownernode.has_ModelWithTag(EModelTag.ORBITAL).call_APIs("get_Position")
        print(pos.to_lat_long(), self.__ownernode.timestamp)

def init_simplemodel(
        _ownernodeins: INode, 
        _loggerins: ILogger, 
        _modelArgs) -> IModel:
    '''
    @desc
        This method initializes an instance of ModelOrbit class
    @param[in]  _ownernodeins
        Instance of the owner node that incorporates this model instance
    @param[in]  _loggerins
        Logger instance
    @param[in]  _modelArgs
        It's a converted JSON object containing the model related info. 
        @key always_calculate
            Wether to automatically update the location of the node at every timestep
    @return
        Instance of the model class
    '''
    # check the arguments
    assert _ownernodeins is not None
    assert _loggerins is not None


    _alwaysCalc = False
    if hasattr(_modelArgs, 'always_calculate'):
        _alwaysCalc = _modelArgs['always_calculate']
    else:
        _loggerins.write_Log("always_calculate not provided provided. Defaulting to False", ELogType.LOGWARN, _ownernodeins.timestamp, "ModelOrbit")
        
    return simplemodel(_ownernodeins, _loggerins, _alwaysCalc)