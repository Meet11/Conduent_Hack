pragma solidity 0.4.25;
pragma experimental ABIEncoderV2;

contract TenderCreate{
    struct Bid{
        address bidder;
        uint256 val;
        
    }
    event GetBidder(address[] bidder_address, uint256[] val_int);

    event Winner(address _address, uint256 _value);
    
    mapping (address=>bool) bidder_check;
   
    string public tenderSector;
    string public location;
    uint256 public tenderMinVal;
    uint256 public refNumber;
    string public startDate;
    address public owner;
   
    address[] verifiedAddress;
   
    Bid[] public  bidAddress;
   
    function TenderCreate(string memory _tenderSector, string memory _location, uint256 val, uint256 refNo, string memory _startDate) public{
        owner = msg.sender;
        tenderSector = _tenderSector;
        location = _location;
        tenderMinVal = val;
        refNumber = refNo;
        startDate = _startDate;
    }
   
   
    function getbidder() public returns (address[] memory, uint256[] memory) {
        address[] memory addrs = new address[](bidAddress.length);
        uint[] memory val = new uint[](bidAddress.length);

        for (uint i = 0; i < bidAddress.length; i++) {
            Bid storage bid = bidAddress[i];
            addrs[i] = bid.bidder;
            val[i] = bid.val;
        }
        emit GetBidder(addrs, val);
        return (addrs, val);
    }
   
   
    function verifyBidder(address bidder) public{
        verifiedAddress.push(bidder);
    }
   
   
    function check(address bidder) internal view returns(bool){
        for(uint256 i = 0; i < verifiedAddress.length; i++){
            if(bidder == verifiedAddress[i]){
                return true;
            }
        }
        return false;
    }
   
   
    function performBid(uint256 _bidPrice) public returns(bool){
        if(check(msg.sender)){
            if(bidder_check[msg.sender]==true)
                throw;
            require(_bidPrice > tenderMinVal);
            uint lastIndex = bidAddress.length - 1;
            bidAddress.push(Bid(msg.sender, _bidPrice));
            bidder_check[msg.sender] = true;
            
            return true;
        }
    }
   
   
    function sort() public returns(Bid memory){
        Bid memory bidder = bidAddress[0];
        uint256 max = bidAddress[0].val;
        for(uint i = 1; i < bidAddress.length; i++){
            if(bidAddress[i].val > max){
                max = bidAddress[i].val;
                bidder = bidAddress[i];
            }
        }
        return bidder;
    }
   
   
    function setWinner() public returns(address, uint256){
        require(msg.sender == owner);
        Bid memory win = sort();
        emit Winner(win.bidder, win.val);
        return (win.bidder,win.val);
    }
   
}